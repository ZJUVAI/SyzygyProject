"""Damage saved witnesses to check that validators reject them."""
import json


def broken(task, solution):
    s=json.loads(json.dumps(solution))
    if task=='T024': s['points']=[[0, 0], [0, 0]]
    elif task=='T084': s['pairs'][0]=[1, 1]
    elif task=='T010': s['placements'][0]['x']=s['width']
    elif task=='T036': s['edges'].append(list(s['edges'][0]))
    elif task=='T009': s['squares'][0][0]=s['side']
    elif task=='T028': s['edges'].append(dict(s['edges'][0]))
    elif task=='T027': s['edges']=s['edges'][:-1]
    elif task=='T029': s['polygons']=[]
    elif task=='T082': s['coefficients']=[1]+[0]*230
    elif task=='T006':
        s['item_indices']=[0];s['x_translations']=[10**15];s['y_translations']=[0]
    elif task=='T055': s['rows'][0]^=1
    elif task in ('T075', 'T074', 'T073'): s['sequence'][0]=0
    elif task=='T081': s['coefficients']=[1]
    elif task=='T044': s['ordering'][0]=s['ordering'][1]
    elif task=='T079': s['heights']=[0]*480
    elif task=='T007': s['radius']='100'
    elif task in ('T061', 'T072'): s['elements'][1]=s['elements'][0]
    elif task=='T005': s['triangles'][1]=s['triangles'][0]
    elif task=='T045': s['black'][0]=s['white'][0]
    elif task in ('T076','T078','T077'): s['coefficients']=[0]*len(s['coefficients'])
    elif task in ('T067', 'T038'): s['colors']=[0]*len(s['colors'])
    elif task in ('T093','T094'): s['permutation'][1]=s['permutation'][0]
    elif task=='T086': s['terms'][1]=s['terms'][0]
    elif task=='T100': s['word']='1234567'
    elif task=='T042': s['labels'][0]=2
    elif task=='T068': s.update(n=7, colors=[0]*7)
    elif task=='T019': s['points']=[[i,i*i] for i in range(7)]
    elif task in ('T025', 'T022', 'T016', 'T018', 'T023', 'T021', 'T020', 'T011', 'T012', 'T017', 'T065'): s['points'][1]=s['points'][0]
    elif task=='T013': s['directions'][1]=s['directions'][0]
    elif task in ('T056', 'T008'): s['squares'].append(s['squares'][0])
    elif task=='T049': s['codewords']=[0,1]
    elif task=='T096': s['tour'][1]=s['tour'][0]
    elif task=='T050': s['codewords']=[]
    elif task=='T048': s['codewords']=['00000000000011111','00000000000101111']
    elif task=='T066': s['lines'][1]=s['lines'][0]
    elif task=='T014': s['gram'][0][0]=0
    elif task in ('T070','T071'): s['set'][1]=s['set'][0]
    elif task=='T037': s['edges']=[[0,1,2],[0,1,3],[0,2,3]]
    elif task=='T062': s['elements']=[1,2,3]+[2**i for i in range(3,15)]
    elif task in ('T026', 'T030'): s['edges'].pop()
    elif task=='T064': s['elements']=[1,2]
    elif task=='T092': s['coefficients_ascending']=[0]*101
    elif task=='T035': s['edges']=[[i,(i+1)%6] for i in range(6)]
    elif task=='T089': s['expression']+=' + 1'
    elif task=='T057': s['rounds'].append(s['rounds'][0])
    elif task=='T039': s['vertices'].append(s['vertices'][0])
    elif task=='T097': s['routes'].append(s['routes'][0][:])
    elif task=='T098': s['assignment']=[False]*1630
    elif task=='T095': s['machine_orders'][0][1]=s['machine_orders'][0][0]
    elif task=='T090': s['factors'][0]*=2
    elif task=='T083': s['sequence']=[1]*4
    elif task=='T052': s['codewords']=[list(range(12)),list(range(12))]
    elif task=='T041': s['vertices']=[0,1,3,2]
    elif task=='T099': s['comparators']=[]
    elif task=='T060': s['basis']=[0,6166]
    elif task=='T091': s['coefficients']=[0]
    elif task=='T043': s['ordering'][1]=s['ordering'][0]
    elif task=='T031': s['edges'].append([0,0])
    elif task=='T051': s['codewords']=[ [1,2,4], [1,2,8] ]
    elif task=='T063': s['elements']=[1,2,3]
    elif task in ('T004', 'T003'): s['squares'][1]=s['squares'][0]
    elif task=='T015':
        key='points' if 'points' in s else 'stereographic'
        s[key][1]=s[key][0]
    elif task=='T059': s['rows'][0][1]=s['rows'][0][0]
    elif task=='T034':
        for i in range(3):
            for j in range(3): s['matrix'][i][j]=1
    elif task=='T080': s['heights'][0]='2'
    elif task=='T001': s['centers'][1]=s['centers'][0]
    elif task=='T002': s['circles'][1]=s['circles'][0]
    elif task in ('T033','T032'): s['adjacency']=[[1]]
    elif task=='T054': s['array']=[]
    elif task=='T053': s['blocks']=[]
    elif task=='T046': s['generator_matrix'][1]=s['generator_matrix'][0]
    elif task=='T047': s['codewords'].append(s['codewords'][0])
    elif task=='T085': s['matrix'][0][0]=0
    else:
        key={'T058':'marks','T069':'set','T040':'words','T087':'tuple','T088':'chain'}[task]
        s[key][1]=s[key][0]
    return s
