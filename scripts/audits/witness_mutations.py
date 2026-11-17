"""Damage saved witnesses to check that validators reject them."""
import json


def broken(task, solution):
    s=json.loads(json.dumps(solution))
    if task=='T101': s['points']=[[0, 0], [0, 0]]
    elif task=='T102': s['pairs'][0]=[1, 1]
    elif task=='T099': s['placements'][0]['x']=s['width']
    elif task=='T100': s['edges'].append(list(s['edges'][0]))
    elif task=='T098': s['squares'][0][0]=s['side']
    elif task=='T095': s['edges'].append(dict(s['edges'][0]))
    elif task=='T094': s['edges']=s['edges'][:-1]
    elif task=='T097': s['polygons']=[]
    elif task=='T092': s['coefficients']=[1]+[0]*230
    elif task=='T093':
        s['item_indices']=[0];s['x_translations']=[10**15];s['y_translations']=[0]
    elif task=='T091': s['rows'][0]^=1
    elif task in ('T090', 'T054', 'T013'): s['sequence'][0]=0
    elif task=='T089': s['coefficients']=[1]
    elif task=='T088': s['ordering'][0]=s['ordering'][1]
    elif task=='T087': s['heights']=[0]*480
    elif task=='T085': s['radius']='100'
    elif task in ('T084', 'T072'): s['elements'][1]=s['elements'][0]
    elif task=='T083': s['triangles'][1]=s['triangles'][0]
    elif task=='T082': s['black'][0]=s['white'][0]
    elif task in ('T014','T015','T016'): s['coefficients']=[0]*len(s['coefficients'])
    elif task in ('T026', 'T030'): s['colors']=[0]*len(s['colors'])
    elif task in ('T027','T028'): s['permutation'][1]=s['permutation'][0]
    elif task=='T029': s['terms'][1]=s['terms'][0]
    elif task=='T031': s['word']='1234567'
    elif task=='T033': s['labels'][0]=2
    elif task=='T034': s.update(n=7, colors=[0]*7)
    elif task=='T035': s['points']=[[i,i*i] for i in range(7)]
    elif task in ('T036', 'T066', 'T073', 'T074', 'T081', 'T065', 'T049', 'T004', 'T021', 'T005', 'T025'): s['points'][1]=s['points'][0]
    elif task=='T037': s['directions'][1]=s['directions'][0]
    elif task in ('T038', 'T070'): s['squares'].append(s['squares'][0])
    elif task=='T071': s['codewords']=[0,1]
    elif task=='T069': s['tour'][1]=s['tour'][0]
    elif task=='T068': s['codewords']=[]
    elif task=='T067': s['codewords']=['00000000000011111','00000000000101111']
    elif task=='T079': s['lines'][1]=s['lines'][0]
    elif task=='T078': s['gram'][0][0]=0
    elif task in ('T077','T080'): s['set'][1]=s['set'][0]
    elif task=='T075': s['edges']=[[0,1,2],[0,1,3],[0,2,3]]
    elif task=='T076': s['elements']=[1,2,3]+[2**i for i in range(3,15)]
    elif task in ('T064', 'T006'): s['edges'].pop()
    elif task=='T062': s['elements']=[1,2]
    elif task=='T063': s['coefficients_ascending']=[0]*101
    elif task=='T061': s['edges']=[[i,(i+1)%6] for i in range(6)]
    elif task=='T060': s['expression']+=' + 1'
    elif task=='T058': s['rounds'].append(s['rounds'][0])
    elif task=='T059': s['vertices'].append(s['vertices'][0])
    elif task=='T057': s['routes'].append(s['routes'][0][:])
    elif task=='T055': s['assignment']=[False]*1630
    elif task=='T056': s['machine_orders'][0][1]=s['machine_orders'][0][0]
    elif task=='T053': s['factors'][0]*=2
    elif task=='T051': s['sequence']=[1]*4
    elif task=='T052': s['codewords']=[list(range(12)),list(range(12))]
    elif task=='T050': s['vertices']=[0,1,3,2]
    elif task=='T048': s['comparators']=[]
    elif task=='T047': s['basis']=[0,6166]
    elif task=='T046': s['coefficients']=[0]
    elif task=='T045': s['ordering'][1]=s['ordering'][0]
    elif task=='T044': s['edges'].append([0,0])
    elif task=='T043': s['codewords']=[ [1,2,4], [1,2,8] ]
    elif task=='T042': s['elements']=[1,2,3]
    elif task in ('T041', 'T002'): s['squares'][1]=s['squares'][0]
    elif task=='T040':
        key='points' if 'points' in s else 'stereographic'
        s[key][1]=s[key][0]
    elif task=='T039': s['rows'][0][1]=s['rows'][0][0]
    elif task=='T032':
        for i in range(3):
            for j in range(3): s['matrix'][i][j]=1
    elif task=='T017': s['heights'][0]='2'
    elif task=='T001': s['centers'][1]=s['centers'][0]
    elif task=='T003': s['circles'][1]=s['circles'][0]
    elif task in ('T024','T022'): s['adjacency']=[[1]]
    elif task=='T023': s['array']=[]
    elif task=='T008': s['blocks']=[]
    elif task=='T009': s['generator_matrix'][1]=s['generator_matrix'][0]
    elif task=='T010': s['codewords'].append(s['codewords'][0])
    elif task=='T018': s['matrix'][0][0]=0
    else:
        key={'T007':'marks','T012':'set','T011':'words','T019':'tuple','T020':'chain'}[task]
        s[key][1]=s[key][0]
    return s
