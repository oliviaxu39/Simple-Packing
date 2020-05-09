'''
This script converts pdb files to density maps
'''

op = {'situs_pdb2vol_program':'/shared/opt/local/img/em/et/util/situs/Situs_2.7.2/bin/pdb2vol', 'spacing_s': [10.0], 'resolution_s':[10.0], 'pdb_dir':'../IOfile/pdbfile', 'out_file':'IOfile/map_single/situs_maps.pickle'}

def pdb2map(op):
    # convert to density maps
    import aitom.structure.pdb.situs_pdb2vol__batch as TSPS
    ms = TSPS.batch_processing(op)

    # use resize_center_batch_dict() to change maps into same size
    ms = {_: ms[_][10.0][10.0]['map'] for _ in ms}
    import numpy as np
    for n in ms:
        print(n, np.shape(ms[n]))
    import tomominer.image.vol.util as TIVU
    ms = TIVU.resize_center_batch_dict(vs=ms, cval=0.0)
    print('#resize#')
    for n in ms:
        print(n, np.shape(ms[n]))

    return ms

if __name__ == '__main__':
    ms = pdb2map(op)
    import iomap as IM
    for n in ms:
        v = ms[n]
        IM.map2mrc(v, '../map_single/{}.mrc'.format(n))

    data = {}
    i = 0
    for n in ms:
        data[i] = {n:ms[n]}
        i = i + 1
    np.save('data.npy', data)