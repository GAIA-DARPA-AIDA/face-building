dataName = 'm18'
dataName2 = 'm18_f'
import sys

parent_file = sys.argv[1]#'/home/brian/facenet-master/results/parent_'+dataName+'.tab' 
video_frame_mapping = sys.argv[2]#'/dvmm-filer2/projects/AIDA/data/ldc_eval_m18/LDC2019E42 \
#_AIDA_Phase_1_Evaluation_Source_Data_V1.0/docs/masterShotBoundary.msb'
face_img_result =  sys.argv[3] + '.p'#= '/home/brian/facenet-master/results/result_'+dataName+'.p'
face_frame_result = sys.argv[4] + '.p'#= '/home/brian/facenet-master/results/result_'+dataName2+'.p'
bbox_img = sys.argv[5] + '.pickle' #'/home/brian/facenet-master/results/bbox_'+dataName+'.pickle'
bbox_frame = sys.argv[6] + '.pickle'#'/home/brian/facenet-master/results/bbox_'+dataName2+'.pickle'
az_obj_graph = sys.argv[7]#'/home/brian/facenet-master/results/rdf_graphs_34.pkl'
az_obj_jpg = sys.argv[8]#'/home/brian/facenet-master/results/det_results_merged_34a_jpg.pkl'
az_obj_kf = sys.argv[9]#'/home/brian/facenet-master/results/det_results_merged_34b_kf.pkl'
Lorelei_path = sys.argv[10]#'/home/brian/facenet-master/LDC2018E80_LORELEI_Background_KB/data/entities.tab'
#flag_result = sys.argv[11]#'/home/brian/tensorflow-retrain-sample/flag_m18_2.pickle'
#landmark_result = sys.argv[12]#'/home/brian/tensorflow/models/research/delf/delf/python/examples/result_dic_m18_new.p'
RPI_entity = sys.argv[11]#'/home/brian/facenet-master/results/PT003_r1.pickle'
#input_img_path = sys.argv[14]#'/home/brian/facenet-master/datasets/m18/m18/'
ttl_out = sys.argv[12]#'/home/brian/facenet-master/datasets/m18/m18/'
#outputN = 'm18_vision'
print(ttl_out)  
import time

start = time.time()
from multiprocessing import Pool 
from collections import defaultdict
from collections import Counter
import pickle
import cv2
import numpy as np
from PIL import Image
#import visualization_utils
import scipy.misc
from glob import glob
import operator
import json
import sys
import os
import pickle
import csv
from io import BytesIO
import numpy as np
#sys.path.append("AIDA-Interchange-Format/python")
#sys.path.append("/home/brian/AIDA-Interchange-Format/python")

from io import BytesIO
from rdflib import Graph, URIRef, RDF

from aida_interchange import aifutils
from aida_interchange.bounding_box import Bounding_Box
from aida_interchange.ldc_time_component import LDCTimeComponent, LDCTimeType
from aida_interchange.rdf_ontologies import ldc_ontology_m36, interchange_ontology

from sklearn.cluster import DBSCAN
import sys


    
 
#if dataName == 'dry3':
child = defaultdict(list)
file5= open(parent_file, encoding="utf-8")
i = 0
for line in file5:
    i+=1
    if i ==1:
        continue
    data = line.split()
    child[data[2]].append(data[3])
#print(child)
with open(bbox_img, 'rb') as handle:
    bb = pickle.load(handle)
with open(bbox_frame, 'rb') as handle:
    bb_2 = pickle.load(handle)


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True




with open(face_img_result, 'rb') as handle:
    result = pickle.load(handle, encoding="latin1")
        
with open(face_frame_result, 'rb') as handle:
    result2 = pickle.load(handle, encoding="latin1")

#if dataName == 'dry3':
with open(az_obj_graph , 'rb') as handle:
    (kb_dict, entity_dict, event_dict) = pickle.load(handle)
#print(kb_dict)
with open(az_obj_jpg , 'rb') as handle:
    OD_result = pickle.load(handle)

with open(az_obj_kf , 'rb') as handle:
    ODF_result = pickle.load(handle)
    
entity_dic2 = defaultdict(list)
for x,y in entity_dict.items():
    data = x.split('/')
    #print data
    entity_dic2[data[-2]].append(int(data[-1]))
    
#nameSet = set()
nameList = []
total_score = []
scoreD_t = []



#print terms
clusterDic = {}

#if dataName == 'dry3':
file1 = open(video_frame_mapping)
videoDic = {}
for line in file1:
    data = line.split()
    videoDic[data[0]] = data[1].split('_')[0]
    
#print videoDic

category_index = {}
index_category = {}
i=0

file1 = open('per_list.txt', encoding="utf-8")    

nameSet = set()

for line in file1:
    data = line.replace('\n','')
    

    nameSet.add(data)
#print(nameSet)

for name in nameSet:
    #print name
    #data = name.split('/')[-1]
    #if data not in deleteSet:
    #   continue
    #print(data)
    i+=1

    category_index[i] = {'id': i, 'name': name}
    index_category[name] = i

entity_dic2 = defaultdict(list)
for x,y in entity_dict.items():
    data = x.split('/')
    #print data
    entity_dic2[data[-2]].append(int(data[-1]))
import json
#from pprint import pprint


i=0
from collections import defaultdict
id2Name = defaultdict(list)
name2ID = {}
file1 = open(Lorelei_path, encoding="utf-8")
for line in file1:
    data = line.split('\t')
    i+=1
    #print data
    #if i == 10:
    #    break
    if data[1] == 'PER':
        #print line
        id2Name[data[2]].append(data[3].lower())
        name2ID[data[3].lower()] = data[2]
        #break

#with open('tempname2ID.pickle', 'rb') as handle:
#    name2ID = pickle.load(handle)
    

"""
with open(flag_result, 'rb') as handle:
    flag_dict_s = pickle.load(handle)
with open(landmark_result, 'rb') as f:
    landmark_dict2 = pickle.load(f,encoding='utf-8')
    #u = pickle._Unpickler(f)
    #u.encoding = 'latin1'
    #landmark_dict2 = u.load()
landmark_dict = {}
for x,y in landmark_dict2.items():
    try:
        #print(x)
        print(y)
        landmark_dict[x] = y
    except:
        aaaaa=0
        #print('error')

landmark_id = {}
landmarkSet = set()
count=0
for x,y in landmark_dict.items():
    #print (x,y)
    if y not in landmarkSet and y!='':
        landmarkSet.add(y)
        landmark_id[y] = count
        count+=1
#print(landmark_dict)
#print(landmark_id)
    #break
#building_dry = ['IC0011UWP','IC0011VOR','IC0011WXU','IC0011XEN','IC0011XEO','IC0014YXH','IC0014ZPU']
#nameSet_b =set()
#nameSet_b.add('Maidan_Nezalezhnosti')
"""

#print ID2name[5601538]
import pickle
with open(RPI_entity, 'rb') as handle:
    RPI = pickle.load(handle)

import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))





    
def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    #iou = interArea / float(boxAArea + boxBArea - interArea)
    iou = interArea / float(boxBArea)

    # return the intersection over union value
    return iou

import random
import multiprocessing as mp
from scipy import spatial

docNum = 0

g_dic = {}
entityDic ={}
entityDic_b = {}
nameCount2 = 0
chi_set = set()
parent_set = set()
person_set = set()
total_key = set()
doc_N = set()
img_N = set()
clusterDic_b = {}
#
kb_dict_bf = {}

directory = ttl_out#+'/'
if not os.path.exists(directory):
    os.makedirs(directory)
print(directory)

def link_to_obj(key, g, entity,x,person_c_n):
    sys = aifutils.make_system_with_uri(g, "http://www.columbia.edu/AIDA/DVMM/Systems/Face/FaceNet")

    person_label = ['/m/01g317','/m/04yx4','/m/03bt1vf','/m/01bl7v','/m/05r655','/m/04hgtk','/m/01bgsw']
    first_cluster = 1
    if key in OD_result.keys():
        for n in range(len(OD_result[key])):

            #print OD_result[key][n]['label']
            if OD_result[key][n]['label'] in person_label:
                #print OD_result[key][n]['label']
                boxA = OD_result[key][n]['bbox']
                boxB = (int(bb[x][0]),int(bb[x][1]),int(bb[x][2]),int(bb[x][3]))
                IOA = bb_intersection_over_union(boxA, boxB)
                if IOA > 0.9:

                    eid = "http://www.columbia.edu/AIDA/DVMM/Entities/ObjectDetection/RUN00010/JPG/"+key+"/"+str(n)
                    #print entity_dic2[key]
                    #print n
                    if n in entity_dic2[key]:
                    #if eid in entity_dict.keys():
                        score = IOA

                        #eid_list.append(eid)
                        if first_cluster == 1:

                            first_cluster = 0
                            clusterName = aifutils.make_cluster_with_prototype(g, \
                            "http://www.columbia.edu/AIDA/DVMM/Clusters/HumanBody/RUN00010/JPG/"\
                            +key+"/"+str(n)+"/"+str(person_c_n),entity, sys)

                        aifutils.mark_as_possible_cluster_member(g, \
                                entity_dict[eid],clusterName, score, sys)

        if first_cluster == 0:

            person_c_n+=1
    return person_c_n, g

    
def transferAIF(parent):
    chi = child[parent]
    
    if parent in kb_dict.keys():
        print(parent)
        g = kb_dict[parent]
        g.bind('ldcOnt', ldc_ontology_m36.NAMESPACE)

 
    else:
        print('not Graph')
        g = aifutils.make_graph()
        g.bind('ldcOnt', ldc_ontology_m36.NAMESPACE)
    #"""                                  
    #=============face recognition=============
    sys = aifutils.make_system_with_uri(g, "http://www.columbia.edu/AIDA/DVMM/Systems/Face/FaceNet")

    NameDetected = set()
    NameDetected_score = {}
    nameCount = Counter()
    count = 0
    c_num = 0
    person_c_n = 0
    #print comblineSet
    In = 0
    #print bb
    featureDic = {}
    first = 1
    entityList = []
    arrayList = []
    person_label = ['/m/01g317','/m/04yx4','/m/03bt1vf','/m/01bl7v','/m/05r655','/m/04hgtk','/m/01bgsw']
    for x, y in result.items():
        #print x
        data = x.split('/')[-1]
        if '._' in data:
            continue
        data2 = data.split('_')
        #print data2[0]
        #print data2[1][:-4]
        key = data2[0]
        i = data2[1][:-4]
        #print chi
        #print key
        
        if key not in chi:
            continue
        if  float(y[1])<0.04 :
      
            continue
        else:
            NameDetected.add(y[0].replace(' ','_'))
            score = float(y[1])+0.5
            NameDetected_score[y[0].replace(' ','_')] = min(1,score)
            
    for x, y in result2.items():
        #print x
        data = x.split('/')[-2]
        if '._' in data:
            continue

        data = x.split('/')[-1]
        data2 = data.split('_')
        key = x.split('/')[-2]
        
        if videoDic[key] not in chi:
            continue
            
        if float(y[1])<0.04:
            continue
        else:    
            NameDetected.add(y[0].replace(' ','_'))
            score = float(y[1])+0.5
            NameDetected_score[y[0].replace(' ','_')] = min(1,score)
            
    for key, value in index_category.items(): #key name. value is number
        if key not in NameDetected:
            continue
        key = key.replace(' ','_')
        
        #keu = entityDic
        name = "http://www.columbia.edu/AIDA/DVMM/Entities/FaceID/"+str(value)+'/'+key
        entity = aifutils.make_entity(g, name, sys)
        entityDic[key] = entity
        #print AIDA_PROGRAM_ONTOLOGY2.term('Person')
        #score = NameDetected_score[key]
        type_assertion = aifutils.mark_type(g, \
            "http://www.columbia.edu/AIDA/DVMM/TypeAssertion/FaceID/"\
            +str(value)+'/'+key, entity, ldc_ontology_m36.PER, sys, 1)

        new_key = key.lower().replace('_',' ')
        if new_key in name2ID.keys():
            aifutils.link_to_external_kb(g, entity, "REFKB:"+name2ID[new_key], sys, 1)
            #print 'Lorelei'
            #print parent
        else:
            a = 0
            #print 'dbpedia'
            #print parent
            #aifutils.link_to_external_kb(g, entity, VIS_ONTOLOGY2.term(key) , sys, 1)
            aifutils.link_to_external_kb(g, entity, 'http://dbpedia.org/resource/'+key, sys, 1)
    for x, y in result.items():
        #print x

        data = x.split('/')[-1]
        if '._' in data:
            continue
        data2 = data.split('_')
        #print data2[0]
        #print data2[1][:-4]
        key = data2[0]
        i = data2[1][:-4]
        #print chi
        #print key
        
        if key not in chi:
            continue
        #print chi
        #print key
        In = 1

        

               
        
        #======================== JPG ===============
        #eid_list = []
        
        

        l,t,r,d = bb[x]
        if (r-l)*(d-t)<4800:
            continue



        bb2 = Bounding_Box((bb[x][0], bb[x][1]), (bb[x][2], bb[x][3]))
        
        
     
        if float(y[1])<0.04: 
            name = "http://www.columbia.edu/AIDA/DVMM/Entities/FaceDetection/RUN00010/"+str(key)+'/'+str(i)
            #entityList.append(key)
            #entityList.append(entity)
            entity = aifutils.make_entity(g, name, sys)
            entityList.append(entity) 
            arrayList.append(y[2])
            feature = {}
            feature['columbia_vector_faceID_FaceNet'] = y[2].tolist()
            json_data = json.dumps(feature)
            aifutils.mark_private_data(g, entity, json_data, sys)
            #labelrdf = VIS_ONTOLOGY.term(i_id)
            #Dscore = value[i][7]
            #if Dscore>1:
            Dscore=1
            #type_assertion = aifutils.mark_type(g, "Columbia/DVMM/TypeAssertion/FaceRecognition/RUN00003/"+str(i_id)+"/"+str(i)+"/1", 
            type_assertion = aifutils.mark_type(g, \
            "http://www.columbia.edu/AIDA/DVMM/TypeAssertion/FaceDetection/RUN00010/JPG/"+\
                str(key)+'/'+str(i), entity, ldc_ontology_m36.PER, sys, Dscore)
            justif = aifutils.mark_image_justification(g, [entity, type_assertion], key, bb2, sys, 1)
            aifutils.add_source_document_to_justification(g, justif, parent)
            aifutils.mark_informative_justification(g, entity, justif)
            chi_set.add(key)
            parent_set.add(parent)
            person_c_n, g = link_to_obj(key,g,entity,x,person_c_n)
        else:
            #nameCount2+=1
            person_set.add(y[0].replace(' ','_'))
            doc_N.add(parent)
            img_N.add(key)

            score = sigmoid(float(y[1])*10)
 
            NameDetected.add(y[0].replace(' ','_'))
            #print y[0].replace(' ','_')
            entity_key = y[0].replace(' ','_')
            type_assertion = aifutils.mark_type(g, \
            "http://www.columbia.edu/AIDA/DVMM/TypeAssertion/FaceID/"\
            +str(index_category[entity_key])+'/'+entity_key, entityDic[entity_key], ldc_ontology_m36.PER, sys, 1)

            justif = aifutils.mark_image_justification(g, [entityDic[y[0].replace(' ','_')], \
                                                           type_assertion], key, bb2, sys, score)
            aifutils.add_source_document_to_justification(g, justif, parent)
            aifutils.mark_informative_justification(g, entityDic[y[0].replace(' ','_')], justif)

            person_c_n, g = link_to_obj(key,g,entityDic[y[0].replace(' ','_')],x, person_c_n)
            
            #                                    entity, labelrdf, sys, score)

            #print str(value[i][2]).replace("L",'')

    #========================== Video Frame ================
    for x, y in result2.items():
        #print x
        data = x.split('/')[-2]
        if '._' in data:
            continue

        data = x.split('/')[-1]
        data2 = data.split('_')
        key = x.split('/')[-2]
        
        if videoDic[key] not in chi:
            continue
        #print "video"
        In = 1
        i = data2[-1][:-4]
        frame = data[:-len(data2[-1])-1]
        frameNum = frame.split('_')[-1]

        

        

        #txn.put("Columbia/DVMM/TypeAssertion/FaceID/RUN00003/"+str(key)+'/'+str(i), value[i][4]);
        #featureDic[entity] = y[2]
        featureDic[key] = y[2]
 
        #entityList.append(key)
        l,t,r,d = bb_2[x]
        if (r-l)*(d-t)<4800:
            continue
        bb2 = Bounding_Box((bb_2[x][0], bb_2[x][1]), (bb_2[x][2], bb_2[x][3]))
        
        if float(y[1])<0.04:
            name = "http://www.columbia.edu/AIDA/DVMM/Entities/FaceDetection/RUN00010/Keyframe/"+\
            str(videoDic[key])+'_'+str(frameNum)+'/'+str(i)
            entity = aifutils.make_entity(g, name, sys)
            entityList.append(entity)
            arrayList.append(y[2])
            #if first == 1:
            #    new_array = [y[2]]
            #    first = 0
            #else:
            #    new_array = np.concatenate((new_array, [y[2]]), axis=0)
            feature = {}
            feature['columbia_vector_faceID_FaceNet'] = y[2].tolist()
            json_data = json.dumps(feature)
            aifutils.mark_private_data(g, entity, json_data, sys)
            #labelrdf = VIS_ONTOLOGY.term(i_id)
            #Dscore = value[i][7]
            #if Dscore>1:
            Dscore=1
            #type_assertion = aifutils.mark_type(g, "Columbia/DVMM/TypeAssertion/FaceRecognition/RUN00003/"+str(i_id)+"/"+str(i)+"/1", 
            type_assertion = aifutils.mark_type(g, "http://www.columbia.edu/AIDA/DVMM/TypeAssertion/FaceDetection/RUN00010/Keyframe/"+\
                str(videoDic[key])+'_'+str(frameNum)+'/'+str(i), entity, ldc_ontology_m36.PER, sys, Dscore)
                #str(videoDic[key])+'_'+str(frameNum)+'/'+str(i), entity, AIDA_PROGRAM_ONTOLOGY2.Entity, sys, Dscore)
            #print bb[x][1]
            
            #aifutils.mark_image_justification(g, [entity, type_assertion], key, bb2, sys, 1)
            justif = aifutils.mark_keyframe_video_justification(g, [entity, type_assertion], videoDic[key], \
                                                                str(videoDic[key])+'_'+str(frameNum), bb2, sys, 1)
            aifutils.add_source_document_to_justification(g, justif, parent)
            aifutils.mark_informative_justification(g, entity, justif)
            
            chi_set.add(key)
            parent_set.add(parent)

            if str(videoDic[key])+'_'+str(frameNum) in ODF_result.keys():
                first_cluster = 1

                for n in range(len(ODF_result[str(videoDic[key])+'_'+str(frameNum)])):
          
                    if ODF_result[str(videoDic[key])+'_'+str(frameNum)][n]['label'] in person_label:     

                        boxA = ODF_result[str(videoDic[key])+'_'+str(frameNum)][n]['bbox']
                        boxB = (int(bb_2[x][0]),int(bb_2[x][1]),int(bb_2[x][2]),int(bb_2[x][3]))
                        IOA = bb_intersection_over_union(boxA, boxB)
                        if IOA > 0.9:
        
                            eid = "http://www.columbia.edu/AIDA/DVMM/Entities/ObjectDetection/RUN00010/Keyframe/"+str(videoDic[key])+'_'+str(frameNum)+"/"+str(n)
                            if n in entity_dic2[str(videoDic[key])+'_'+str(frameNum)]:
                            #if eid in entity_dict.keys():
                                score = IOA
                                #print x
                                #print entity_dict[eid]
                                #print n

                                if first_cluster == 1:

                                    first_cluster = 0
                                    clusterName = aifutils.make_cluster_with_prototype(g, \
                                    "http://www.columbia.edu/AIDA/DVMM/Clusters/HumanBody/RUN00010/Keyframe/"+\
                                    str(videoDic[key])+'_'+str(frameNum)+'/'+str(i)+'/'+\
                                    str(person_c_n),entity, sys)
                                    #aifutils.mark_as_possible_cluster_member(g, \
                                    #    entity,clusterName, score, sys)

                                aifutils.mark_as_possible_cluster_member(g, \
                                        entity_dict[eid],clusterName, score, sys)
                if first_cluster == 0:
                    person_c_n+=1
        else:
            #nameCount2+=1
            person_set.add(y[0].replace(' ','_'))
            doc_N.add(parent)
            img_N.add(key)
            #if float(y[1])*10>1:
            #    score = 1-random.random()/10
            #else:
            #    score = float(y[1])*10
            score = sigmoid(float(y[1])*10)
            #place_of_birth_in_louisville_cluster = aifutils.mark_as_possible_cluster_member(g, \
            #    entity,clusterDic[nameDic[y[0].replace(' ','_').replace(' ','_')]], score, sys)
            NameDetected.add(y[0].replace(' ','_'))
            entity_key = y[0].replace(' ','_')
            type_assertion = aifutils.mark_type(g, \
            "http://www.columbia.edu/AIDA/DVMM/TypeAssertion/FaceID/"\
            +str(index_category[entity_key])+'/'+entity_key, entityDic[entity_key], ldc_ontology_m36.PER, sys, 1)
            justif = aifutils.mark_keyframe_video_justification(g, [entityDic[y[0].replace(' ','_')], type_assertion], videoDic[key], \
                                                            str(videoDic[key])+'_'+str(frameNum), bb2, sys, score)
            aifutils.add_source_document_to_justification(g, justif, parent)
            aifutils.mark_informative_justification(g, entityDic[y[0].replace(' ','_')], justif)

            if str(videoDic[key])+'_'+str(frameNum) in ODF_result.keys():
                first_cluster = 1

                for n in range(len(ODF_result[str(videoDic[key])+'_'+str(frameNum)])):
          
                    if ODF_result[str(videoDic[key])+'_'+str(frameNum)][n]['label'] in person_label:     

                        boxA = ODF_result[str(videoDic[key])+'_'+str(frameNum)][n]['bbox']
                        boxB = (int(bb_2[x][0]),int(bb_2[x][1]),int(bb_2[x][2]),int(bb_2[x][3]))
                        IOA = bb_intersection_over_union(boxA, boxB)
                        if IOA > 0.9:
        
                            eid = "http://www.columbia.edu/AIDA/DVMM/Entities/ObjectDetection/RUN00010/Keyframe/"+str(videoDic[key])+'_'+str(frameNum)+"/"+str(n)
                            if n in entity_dic2[str(videoDic[key])+'_'+str(frameNum)]:
                            #if eid in entity_dict.keys():
                                score = IOA
                                #print x
                                #print entity_dict[eid]
                                #print n

                                if first_cluster == 1:

                                    first_cluster = 0
                                    clusterName = aifutils.make_cluster_with_prototype(g, \
                                    "http://www.columbia.edu/AIDA/DVMM/Clusters/HumanBody/RUN00010/Keyframe/"+\
                                    str(videoDic[key])+'_'+str(frameNum)+'/'+str(i)+'/'+\
                                    str(person_c_n),entityDic[y[0].replace(' ','_')], sys)
                                    #aifutils.mark_as_possible_cluster_member(g, \
                                    #    entity,clusterName, score, sys)

                                aifutils.mark_as_possible_cluster_member(g, \
                                        entity_dict[eid],clusterName, score, sys)
                if first_cluster == 0:
                    person_c_n+=1
    #dbscan_run(arrayList,entityList)
    new_array = np.array(arrayList)
    
    if len(arrayList)>1 :

        # Compute DBSCAN
        #if __name__ == '__main__':
        db = DBSCAN(eps=0.55, min_samples=2).fit(new_array)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        #print labels
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        #print entityList
            #print('Estimated number of clusters: %d' % n_clusters_)

        clusterNameDic = {}

        firstMem = [0 for i in range(n_clusters_)]
        firstArray = {}
        for i in range(len(labels)):
            if labels[i] == -1:
                continue
            #print len(labels)
            #print len(entityList)
            #score = 1
            if firstMem[labels[i]] == 0:
                firstMem[labels[i]] = 1
                firstArray[labels[i]] = new_array[i]
                clusterNameDic[labels[i]] = aifutils.make_cluster_with_prototype(g, \
                    "http://www.columbia.edu/AIDA/DVMM/Clusters/FaceCoreference/RUN00010/"+\
                    str(labels[i]),entityList[i], sys)
                #print entityList[a][j]
            else:
                dist = np.linalg.norm(firstArray[labels[i]]- new_array[i])
                if dist>1:
                    score = 0.001
                else:
                    score = 1-dist/2
                #score = sigmoid(dist)
                #print score
                aifutils.mark_as_possible_cluster_member(g, \
                    entityList[i],clusterNameDic[labels[i]], score, sys)
    
    sys = aifutils.make_system_with_uri(g, "http://www.columbia.edu/AIDA/DVMM/Systems/Face/FaceNet")
    for key, value in index_category.items():
        if key not in NameDetected:
            continue
        key = key.replace(' ','_')
        
        #print name2ID[]
        new_key = key.lower().replace('_',' ')
        #print new_key
        try:
            #print RPI[parent].keys()
            #print name2ID[new_key]
            if name2ID[new_key] in RPI[parent].keys():
                print (new_key)
                #print parent
                cluster = aifutils.make_cluster_with_prototype(g, \
                    "http://www.columbia.edu/AIDA/DVMM/Clusters/NamedPersonCoreference/"+\
                    str(value)+'/'+key,entityDic[key], sys)
                score = 1 
                #aifutils.mark_as_possible_cluster_member(g, ,cluster, score, sys)
                for i in range(len(RPI[parent][name2ID[new_key]])):
                    aifutils.mark_as_possible_cluster_member(g, \
                        RPI[parent][name2ID[new_key]][i],cluster, score, sys)
        except KeyError:
            a = 0
    
    
    with open(directory+'/'+parent+'.ttl', 'w') as fout:
        serialization = BytesIO()
        # need .buffer because serialize will write bytes, not str
        g.serialize(destination=serialization, format='turtle')
        fout.write(serialization.getvalue().decode('utf-8'))
    #"""
pool = mp.Pool(processes=40)

res = pool.map(transferAIF, child.keys())

end = time.time()
print(end - start)
print (nameCount2)
print (len(chi_set))
print (len(parent_set))
print (len(person_set))
print (len(total_key))
print (len(doc_N))
print (len(img_N))
