from larcv import larcv
larcv.IOManager
from ROOT import TChain
import numpy as np
import scipy.misc as smp
from matplotlib import pyplot as plt

class ImageWriter(object):
  """
    Prints the highest energy particle to file.

    usage:

    my_image_writer = ImagesWriter(<filename>)
    my_image_write.get_all_particle_images()


    Todo:
    generalize this a bit more
  """
  particles = {'electron':11,
               'muon': 13,
               'gamma': 22,
               'piminus':-211}

  def __init__(self, filename):
    self.filename = filename
    self.roi_tree_name='partroi_tpc_hires_crop_tree'
    self.roi_br_name=roi_tree_name.replace('tree','branch')
    self.roi_ch = TChain(roi_tree_name)
    self.roi_ch.AddFile(self.filename)    


  def get_all_particle_images(self):
    for particle in self.particles:
      self.get_particle_image(particle)

  def get_particle_image(self, particle)
    etoi=[]
    for i in range(roi_ch.GetEntries()):
      roi_ch.GetEntry(i)
      roi_br=getattr(roi_ch, roi_br_name)
      bb_array = roi_br.ROIArray()
      bb = bb_array.at(0)
      # filter on particle type
      if bb.PdgCode()==particles[particle]:
        energy = bb.EnergyInit()
        etoi.append([i,energy])

    sorted_etoi = sorted(etoi, key=lambda x: x[1])[-10:]

    pixel_tree_name='image2d_tpc_hires_crop_tree'
    pixel_ch = TChain(pixel_tree_name)
    pixel_ch.AddFile(self.filename)
    for entry in sorted_etoi:
      pixel_ch.GetEntry(entry[0])
      pixel_br=getattr(pixel_ch, pixel_tree_name.replace('tree','branch'))

      data = np.zeros( (576,576,3), dtype=np.uint8 )
      for k in range(3):
          img = pixel_br.at(k)
          mat=larcv.as_ndarray(img)
          for i in range(576):
            for j in range(576):
                data[j,i,k] = (mat[i,j]+256)/2
                if abs(mat[i,j]) <2:
                  data[j,i,k] = 0

      img = smp.toimage( data )       # Create a PIL image
      img.save('{}-{}-scaled.png'.format(particle, entry[0]))


