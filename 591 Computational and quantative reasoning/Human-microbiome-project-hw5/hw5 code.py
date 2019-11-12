
# coding: utf-8

# In[42]:


# do imports
import numpy as np
np.set_printoptions(precision=3)
import matplotlib.pyplot as plt
import pickle
import scipy
import os
import itertools


# set up file names
otu_table_v13 = 'otu_table_psn_v13.txt'
otu_table_v35 = 'otu_table_psn_v35.txt'
mapping_file_v13 = 'v13_map_uniquebyPSN.txt' 
mapping_file_v35 = 'v35_map_uniquebyPSN.txt'


# In[43]:


# loading the entire otu table
def load_otu_table(file_name):
    with open(file_name) as f:
        f.readline() # remove the first line
        line = f.readline().split('\t') # sample ids
        sample_ids = line[1:-1]
        otu_names = []
        otu_table = []
        otu_taxonomy = []
        for line in f:
            items = line.split('\t')
            otu_names.append(items[0])
            otu_table.append(items[1:-1])
            otu_taxonomy.append(items[-1]) 
    table = np.array(otu_table, dtype='int')
    return (sample_ids, otu_names, table, otu_taxonomy)
(sample_ids_13, otu_names_13, table_13, otu_taxonomy_13) = load_otu_table(otu_table_v13)
(sample_ids_35, otu_names_35, table_35, otu_taxonomy_35) = load_otu_table(otu_table_v35)


common_otu_taxonomy =list(set(otu_taxonomy_13) & set(otu_taxonomy_35)) #Taking intersection and generating common otus


# In[44]:


c_table_13=table_13[[i for i in range(len(otu_taxonomy_13)) if otu_taxonomy_13[i] in common_otu_taxonomy],:]
c_table_35=table_35[[i for i in range(len(otu_taxonomy_35)) if otu_taxonomy_35[i] in common_otu_taxonomy],:]
c_otu_taxonomy_13=[i for i in otu_taxonomy_13 if i in common_otu_taxonomy]
c_otu_taxonomy_35=[i for i in otu_taxonomy_35 if i in common_otu_taxonomy]


# In[45]:


#This function is used to remove duplicates from a list, so input parameter is a list and output is a list with duplicates removed
def remov_dup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


# In[47]:


#Group by level
#Function takes four parameters: 
#table: Table to be grouped at a given level
#otu_taxonomy: otu's <- this is the raw otu from the table which will have length equal to table's number of rows
#common_otu_taxonomy: is the list at which you want to group the table at
#level at which you want to group it at

def table_group_by(table,otu_taxonomy,common_otu_taxonomy,level="dummy"):
    
    if level=="taxa" or level=="dummy":
        #groupings is going to be a list of lists in which will have the indices of otu's corresponding to the otu
        #in common_otu_taxonomy
        
        #For example:
        #otu_taxonomy=['a','b','c','a','b','a']
        #common_otu_taxonomy=['b','a']
        #groupings will be [[1,4],[0,3,5]]
        #The elements of the groupings will be used for grouping the actual table
        groupings=[[]]*len(common_otu_taxonomy)
        for i in range(len(otu_taxonomy)):
            if otu_taxonomy[i] in common_otu_taxonomy:
                    groupings[common_otu_taxonomy.index(otu_taxonomy[i])]=groupings[common_otu_taxonomy.index(otu_taxonomy[i])]+[i]
        result_table=[]    
        for i in range(len(groupings)):
                result_table.append(table[groupings[i],:].sum(axis=0)) # Here is where the sum is happening
        result_table=np.array(result_table, dtype='int')
        return result_table 
                
    elif level=="family":
        otu_taxonomy_group_set=[]
        otu_taxonomy_1=[]
        for i in range(len(otu_taxonomy)):
            flag=0
            for j in otu_taxonomy[i].strip().split(";"):
                if j[0]=="f":
                    flag=1
            if flag==1 and otu_taxonomy[i] in common_otu_taxonomy:
                otu_taxonomy_group_set.append(";".join(otu_taxonomy[i].strip().split(";")[0:5]))
                otu_taxonomy_1.append(";".join(otu_taxonomy[i].strip().split(";")[0:5]))
            else:
                otu_taxonomy_1.append(otu_taxonomy[i])
        otu_taxonomy_group_set=remov_dup(otu_taxonomy_group_set)
        otu_taxonomy_group_set.sort()
        return table_group_by(table,otu_taxonomy_1,otu_taxonomy_group_set,"dummy")
    
    elif level=="genus":
        otu_taxonomy_group_set=[]
        otu_taxonomy_1=[]
        for i in range(len(otu_taxonomy)):
            flag=0
            for j in otu_taxonomy[i].strip().split(";"):
                if j[0]=="g":
                    flag=1
            if flag==1 and otu_taxonomy[i] in common_otu_taxonomy:
                otu_taxonomy_group_set.append(";".join(otu_taxonomy[i].strip().split(";")[0:6]))
                otu_taxonomy_1.append(";".join(otu_taxonomy[i].strip().split(";")[0:6]))
            else:
                otu_taxonomy_1.append(otu_taxonomy[i])
        otu_taxonomy_group_set=remov_dup(otu_taxonomy_group_set)
        otu_taxonomy_group_set.sort()
        return table_group_by(table,otu_taxonomy_1,otu_taxonomy_group_set,"dummy")

    
    elif level=="species":
        otu_taxonomy_group_set=[]
        otu_taxonomy_1=[]
        for i in range(len(otu_taxonomy)):
            flag=0
            for j in otu_taxonomy[i].strip().split(";"):
                if j[0]=="s":
                    flag=1
            if flag==1 and otu_taxonomy[i] in common_otu_taxonomy:
                otu_taxonomy_group_set.append(";".join(otu_taxonomy[i].strip().split(";")[0:7]))
                otu_taxonomy_1.append(";".join(otu_taxonomy[i].strip().split(";")[0:7]))
            else:
                otu_taxonomy_1.append(otu_taxonomy[i])
        otu_taxonomy_group_set=remov_dup(otu_taxonomy_group_set)
        otu_taxonomy_group_set.sort()
        return table_group_by(table,otu_taxonomy_1,otu_taxonomy_group_set,"dummy")             
    
    
#taxa_table_13,otu_taxa_13=table_group_by(c_table_13,c_otu_taxonomy_13,common_otu_taxonomy,"taxa")  
#taxa_table_35,otu_taxa_35=table_group_by(c_table_35,c_otu_taxonomy_35,common_otu_taxonomy,"taxa")   
#family_table_13,otu_family_13=table_group_by(c_table_13,c_otu_taxonomy_13,common_otu_taxonomy,"family")  
#family_table_35,otu_family_35=table_group_by(c_table_35,c_otu_taxonomy_35,common_otu_taxonomy,"family")
#species_table_13,otu_species_13=table_group_by(c_table_13,c_otu_taxonomy_13,common_otu_taxonomy,"species")  
#species_table_35,otu_species_35=table_group_by(c_table_35,c_otu_taxonomy_35,common_otu_taxonomy,"species")
genus_table_13=table_group_by(c_table_13,c_otu_taxonomy_13,common_otu_taxonomy,"genus")  
genus_table_35=table_group_by(c_table_35,c_otu_taxonomy_35,common_otu_taxonomy,"genus")  

print(genus_table_13.shape)
print(genus_table_35.shape)


# In[48]:


# loading mapping file
def load_mapping_file(file_name):
    with open(file_name) as f:
        columns = f.readline().split('\t') # remove heading
        empty_lists = [[] for i in columns]
        meta_data = dict(zip(columns, empty_lists)) # accumulating lists
        for line in f:
            for ind, field in enumerate(line.split('\t')):
                meta_data[columns[ind]].append(field)                
    return meta_data


meta_data_13 = load_mapping_file(mapping_file_v13)
sample_num_13 = len(meta_data_13['#SampleID'])

meta_data_35 = load_mapping_file(mapping_file_v35)
sample_num_35 = len(meta_data_35['#SampleID'])



# all tongue samples
all_toungue_samples_13 = []
for i in range(sample_num_13):
    if meta_data_13['HMPbodysubsite'][i] == 'Tongue_dorsum':
        all_toungue_samples_13.append(meta_data_13['#SampleID'][i])
        
# all tongue samples
all_toungue_samples_35 = []
for i in range(sample_num_35):
    if meta_data_35['HMPbodysubsite'][i] == 'Tongue_dorsum':
        all_toungue_samples_35.append(meta_data_35['#SampleID'][i])

        


# In[49]:


# create all tongue table
at_13 = []
for i, ind in enumerate(sample_ids_13):
    if ind in all_toungue_samples_13: at_13.append(i)
at_13 = genus_table_13[:,at_13]

at_35 = []
for i, ind in enumerate(sample_ids_35):
    if ind in all_toungue_samples_35: at_35.append(i)
at_35 = genus_table_35[:,at_35]

at=np.hstack((at_13,at_35))  


# threshold data
abundance_threshold=10
ind = at.sum(axis=1) > abundance_threshold
at=at[ind,:]
at_13 = at_13[ind,:]
at_35 = at_35[ind,:]
print(at.shape, at_13.shape, at_35.shape)


# normalize data
ra = at/at.sum(axis=0)
r13 = at_13/at_13.sum(axis=0)
r35 = at_35/at_35.sum(axis=0)
ra=np.nan_to_num(ra)
r13=np.nan_to_num(r13)
r35=np.nan_to_num(r35)
# print("Histogram of v13")
# plt.hist(at_13.sum(axis=0))
# plt.figure()
# plt.show()
# plt.clf()
# print("Histogram of normalized v13")
# plt.hist(r13.sum(axis=0))
# plt.show()
# plt.clf()


# compare v13 and c35 regions; attemp 01
print("mean abundance plot")
i = np.arange(r13.shape[0])
plt.plot(i, r35.mean(axis=1), 'm.', i, r13.mean(axis=1), 'b.')
plt.show()
plt.clf()

# too much data at the bottom; try log scale
# need pseudo count 
#Q1 part 2 mean log abundance plot
print("log mean abundance plot")
i = np.arange(r13.shape[0])
pseudo_count = 0.1/np.mean(at.sum(axis=0))
print(pseudo_count)
plt.plot(i, np.log10(r35.mean(axis=1)+pseudo_count), 'm.', i, np.log10(r13.mean(axis=1)+pseudo_count), 'b.')
plt.show()
plt.clf()

# still not good; let's try ranking
# rank abundance Q1a)
print("rank abundance plot")
si = np.argsort(r13.mean(axis=1))[::-1]
plt.plot(i, r35.mean(axis=1)[si], 'm.', i, r13.mean(axis=1)[si], 'b.')
plt.show()
plt.clf()

#  logrank abundance Q1a)
print("logrank abundance plot")
si = np.argsort(r13.mean(axis=1))[::-1]
plt.semilogy(i, r35.mean(axis=1)[si]+pseudo_count, 'm.', i, r13.mean(axis=1)[si]+pseudo_count, 'b.')
plt.show()
plt.clf()

# computing the correlation coeffecient
import scipy.stats # provides easy interface
# mean relative abundance
r, p = scipy.stats.pearsonr(r13.mean(axis=1),r35.mean(axis=1))
print('mean relative abundance: r = {0:.2f}, p = {1:.2f}'.format(r,p))
# log of mean relative abundance
r, p = scipy.stats.pearsonr(np.log(r13.mean(axis=1)+pseudo_count), np.log(r35.mean(axis=1)+pseudo_count))
print('log mean relative abundance: r = {0:.2f}, p = {1:.2f}'.format(r,p))
# mean of log relative abundance
ml13 = np.mean(np.log10(r13+pseudo_count), axis=1)
ml35 = np.mean(np.log10(r35+pseudo_count), axis=1)

r, p = scipy.stats.pearsonr(ml13, ml35)
print('mean log relative abundance: r = {0:.2f}, p = {1:.2f}'.format(r,p))

# pearson correlation with NumPy only
o = np.vstack((r13.mean(axis=1), r35.mean(axis=1)))
print('\nCorrelation Matrix for mean relative abundance:\n', np.corrcoef(o))


# # Familylevel

# In[50]:



family_table_13=table_group_by(c_table_13,c_otu_taxonomy_13,common_otu_taxonomy,"family")  
family_table_35=table_group_by(c_table_35,c_otu_taxonomy_35,common_otu_taxonomy,"family")   

# create all tongue table
at_13 = []
for i, ind in enumerate(sample_ids_13):
    if ind in all_toungue_samples_13: at_13.append(i)
at_13 = family_table_13[:,at_13]

at_35 = []
for i, ind in enumerate(sample_ids_35):
    if ind in all_toungue_samples_35: at_35.append(i)
at_35 = family_table_35[:,at_35]

at=np.hstack((at_13,at_35))  


# threshold data
abundance_threshold = 10
ind = at.sum(axis=1) > abundance_threshold
at=at[ind,:]
at_13 = at_13[ind,:]
at_35 = at_35[ind,:]
print(at.shape, at_13.shape, at_35.shape)


# normalize data
ra = at/at.sum(axis=0)
r13 = at_13/at_13.sum(axis=0)
r35 = at_35/at_35.sum(axis=0)
ra=np.nan_to_num(ra)
r13=np.nan_to_num(r13)
r35=np.nan_to_num(r35)
# print("Histogram of v13")
# plt.hist(at_13.sum(axis=0))
# plt.figure()
# plt.show()
# plt.clf()
# print("Histogram of normalized v13")
# plt.hist(r13.sum(axis=0))
# plt.show()
# plt.clf()


# compare v13 and c35 regions; attemp 01
print("mean abundance plot")
i = np.arange(r13.shape[0])
plt.plot(i, r35.mean(axis=1), 'm.', i, r13.mean(axis=1), 'b.')
plt.show()
plt.clf()

# too much data at the bottom; try log scale
# need pseudo count 
#Q1 part 2 mean log abundance plot
print("log mean abundance plot")
i = np.arange(r13.shape[0])
pseudo_count = 0.1/np.mean(at.sum(axis=0))
print(pseudo_count)
plt.plot(i, np.log10(r35.mean(axis=1)+pseudo_count), 'm.', i, np.log10(r13.mean(axis=1)+pseudo_count), 'b.')
plt.show()
plt.clf()

# still not good; let's try ranking
# rank abundance Q1a)
print("rank abundance plot")
si = np.argsort(r13.mean(axis=1))[::-1]
plt.plot(i, r35.mean(axis=1)[si], 'm.', i, r13.mean(axis=1)[si], 'b.')
plt.show()
plt.clf()

#  logrank abundance Q1a)
print("logrank abundance plot")
si = np.argsort(r13.mean(axis=1))[::-1]
plt.semilogy(i, r35.mean(axis=1)[si]+pseudo_count, 'm.', i, r13.mean(axis=1)[si]+pseudo_count, 'b.')
plt.show()
plt.clf()

# computing the correlation coeffecient
import scipy.stats # provides easy interface
# mean relative abundance
r, p = scipy.stats.pearsonr(r13.mean(axis=1),r35.mean(axis=1))
print('mean relative abundance: r = {0:.2f}, p = {1:.2f}'.format(r,p))
# log of mean relative abundance
r, p = scipy.stats.pearsonr(np.log(r13.mean(axis=1)+pseudo_count), np.log(r35.mean(axis=1)+pseudo_count))
print('log mean relative abundance: r = {0:.2f}, p = {1:.2f}'.format(r,p))
# mean of log relative abundance
ml13 = np.mean(np.log10(r13+pseudo_count), axis=1)
ml35 = np.mean(np.log10(r35+pseudo_count), axis=1)

r, p = scipy.stats.pearsonr(ml13, ml35)
print('mean log relative abundance: r = {0:.2f}, p = {1:.2f}'.format(r,p))

# pearson correlation with NumPy only
o = np.vstack((r13.mean(axis=1), r35.mean(axis=1)))
print('\nCorrelation Matrix for mean relative abundance:\n', np.corrcoef(o))


# # Question 2

# In[10]:


# loading the entire otu table
def load_otu_table(file_name):
    with open(file_name) as f:
        f.readline() # remove the first line
        line = f.readline().split('\t') # sample ids
        sample_ids = line[1:-1]
        otu_names = []
        otu_table = []
        otu_taxonomy = []
        for line in f:
            items = line.split('\t')
            otu_names.append(items[0])
            otu_table.append(items[1:-1])
            otu_taxonomy.append(items[-1]) 
    table = np.array(otu_table, dtype='int')
    return (sample_ids, otu_names, table, otu_taxonomy)
(sample_ids_13, otu_names_13, table_13, otu_taxonomy_13) = load_otu_table(otu_table_v13)

genus_table_13=table_group_by(table_13,otu_taxonomy_13,otu_taxonomy_13,"genus")


# In[18]:


# all tongue samples with more visits
all_stool_samples_13_with_more_visits = []
for i in range(sample_num_13):
    if meta_data_13['HMPbodysubsite'][i] == 'Stool' and meta_data_13['visitno'][i]>'1':
        all_stool_samples_13_with_more_visits.append(meta_data_13['#SampleID'][i])


# In[21]:


print(all_stool_samples_13_with_more_visits)
#Considering first two sample ids from the above list for our analysis: '700024449' and '700024492'


# In[26]:


at_13 = []
for i, ind in enumerate(sample_ids_13):
    if ind in ['700024449','700024492']: at_13.append(i)
at_13_two_people = genus_table_13[:,at_13]


# threshold data
abundance_threshold = 5
ind = at_13_two_people.sum(axis=1) > abundance_threshold
at_13_two_people=at_13_two_people[ind,:]


# normalize data
r13_two_people = at_13_two_people/at_13_two_people.sum(axis=0)


# print("Histogram of v13")
# plt.hist(at_13.sum(axis=0))
# plt.figure()
# plt.show()
# plt.clf()
# print("Histogram of normalized v13")
# plt.hist(r13.sum(axis=0))
# plt.show()
# plt.clf()


i = np.arange(r13_two_people.shape[0])
plt.plot(i, r13_two_people[:,0], 'm.', i, r13_two_people[:,1], 'b.')
plt.show()
plt.clf()


print("log abundance plot of two people")
i = np.arange(r13_two_people.shape[0])
pseudo_count = 0.1/np.mean(at_13_two_people.sum(axis=0))
print(pseudo_count)
plt.plot(i, np.log10(r13_two_people[:,0]+pseudo_count), 'm.', i, np.log10(r13_two_people[:,1]+pseudo_count), 'b.')
plt.show()
plt.clf()


# In[28]:


#By looking at the data, sample ids 700024234 and 700113542 are of the same person whose RSID is 764346198
#so we analyse for this person's log abundances at different times
at_13 = []
for i, ind in enumerate(sample_ids_13):
    if ind in ['700024234', '700113542']: at_13.append(i)
at_13_same_person = genus_table_13[:,at_13]


# threshold data
abundance_threshold = 5
ind = at_13_same_person.sum(axis=1) > abundance_threshold
at_13_same_person=at_13_same_person[ind,:]


# normalize data
r13_same_person = at_13_same_person/at_13_same_person.sum(axis=0)


# print("Histogram of v13")
# plt.hist(at_13.sum(axis=0))
# plt.figure()
# plt.show()
# plt.clf()
# print("Histogram of normalized v13")
# plt.hist(r13.sum(axis=0))
# plt.show()
# plt.clf()


i = np.arange(r13_same_person.shape[0])
plt.plot(i, r13_same_person[:,0], 'm.', i, r13_same_person[:,1], 'b.')
plt.show()
plt.clf()


print("log abundance plot of two people")
i = np.arange(r13_same_person.shape[0])
pseudo_count = 0.1/np.mean(at_13_same_person.sum(axis=0))
print(pseudo_count)
plt.plot(i, np.log10(r13_same_person[:,0]+pseudo_count), 'm.', i, np.log10(r13_same_person[:,1]+pseudo_count), 'b.')
plt.show()
plt.clf()


# In[40]:


# Calculating histogram of correlation coeffecients
# between log-transformed abundances computed for all pairs of different subjects. 
# all stool samples with more visits
all_stool_samples_13 = []
for i in range(sample_num_13):
    if meta_data_13['HMPbodysubsite'][i] == 'Stool':
        all_stool_samples_13.append(meta_data_13['#SampleID'][i])
        
# create all stoool table
at_13 = []
for i, ind in enumerate(sample_ids_13):
    if ind in all_toungue_samples_13: at_13.append(i)
at_13 = genus_table_13[:,at_13]



# threshold data
abundance_threshold = 10
ind = at_13.sum(axis=1) > abundance_threshold
at_13 = at_13[ind,:]
print(at_13.shape)


# normalize data
r13 = at_13/at_13.sum(axis=0)
r13=np.nan_to_num(r13)
pseudo_count = 0.1/np.mean(at.sum(axis=0))
log_abundances=np.log10(r13+pseudo_count)

correl_coef_list=[]
indices_list= np.arange(log_abundances.shape[1])
for pair in itertools.combinations(indices_list,2):
    correl_coef_list=correl_coef_list+[scipy.stats.pearsonr(log_abundances[:,pair[0]],log_abundances[:,pair[1]])[0]]

print('histogram of correlation coeffecients of different pair of subjects')
plt.hist(correl_coef_list)
plt.show()
plt.clf()


# # Question 3

# In[31]:


# loading the entire otu table
def load_otu_table(file_name):
    with open(file_name) as f:
        f.readline() # remove the first line
        line = f.readline().split('\t') # sample ids
        sample_ids = line[1:-1]
        otu_names = []
        otu_table = []
        otu_taxonomy = []
        for line in f:
            items = line.split('\t')
            otu_names.append(items[0])
            otu_table.append(items[1:-1])
            otu_taxonomy.append(items[-1]) 
    table = np.array(otu_table, dtype='int')
    return (sample_ids, otu_names, table, otu_taxonomy)
(sample_ids_35, otu_names_35, table_35, otu_taxonomy_35) = load_otu_table(otu_table_v35)

genus_table_35=table_group_by(table_35,otu_taxonomy_35,otu_taxonomy_35,"genus")
print(len(table_35[0]))
def diversity(site):
    # all tongue samples
    
    all_site_samples_35 = []
    for i in range(sample_num_35):
        if meta_data_35['HMPbodysubsite'][i] == site:
            all_site_samples_35.append(meta_data_35['#SampleID'][i])
    table_copy= genus_table_35.copy()
    
    at_35=[]
    for i, ind in enumerate(sample_ids_35):
        if ind in all_site_samples_35: at_35.append(i)
    table_copy = table_copy[:,at_35]
#             table_copy[:,i]=0
    
    abundance_threshold = 10
    ind = table_copy.sum(axis=1) > abundance_threshold
    table_copy=table_copy[ind,:]

    at_35 = table_copy.sum(axis=0)
#     print(table_copy.shape)
#     print(len(at_35))
    result=np.mean(at_35)
    return result


# In[32]:


diversity_dict={}
list_of_sites=list(set(meta_data_35['HMPbodysubsite']))
for site in list_of_sites:
    diversity_dict[site]=diversity(site)
    
diversity_dict

#'Left_Antecubital_fossa' has got most minimum diversity
#'Posterior_fornix' has got maximum diversity


# # Rank Abundance plot for Least and Most diversity sites

# In[33]:


def return_table(site1):

    all_site_samples_35 = []
    for i in range(sample_num_35):
        if meta_data_35['HMPbodysubsite'][i] == site1:
            all_site_samples_35.append(meta_data_35['#SampleID'][i])
    table_copy= genus_table_35.copy()
    
    at_35=[]
    for i, ind in enumerate(sample_ids_35):
        if ind in all_site_samples_35: at_35.append(i)
    table_copy = table_copy[:,at_35]
    
    return table_copy

min_site_table=return_table("Left_Antecubital_fossa")
max_site_table=return_table("Posterior_fornix")
    
    
pseudo_count = 0.1/np.mean(np.hstack((min_site_table,max_site_table)).sum(axis=0))    

# still not good; let's try ranking
# rank abundance Q1a)
print("rank abundance plot")
i=np.arange(min_site_table.shape[0])
si = np.argsort(min_site_table.mean(axis=1))[::-1]
plt.plot(i, max_site_table.mean(axis=1)[si], 'm.', i, min_site_table.mean(axis=1)[si], 'b.')
plt.show()
plt.clf()

#  logrank abundance Q1a)
print("logrank abundance plot")   
si = np.argsort(min_site_table.mean(axis=1))[::-1]
plt.semilogy(i, max_site_table.mean(axis=1)[si]+pseudo_count, 'm.', i, min_site_table.mean(axis=1)[si]+pseudo_count, 'b.')
plt.show()
plt.clf()


# In[34]:


mean_log_abundance_dict={}

for site in list_of_sites:
    mean_log_abundance_dict[site]=np.log10(return_table(site).mean(axis=1)+(0.1/np.mean(return_table(site).sum(axis=0))))

i=0
j=0
correl_list = [[0 for i in range(len(list_of_sites))] for j in range(len(list_of_sites))]
for pair in itertools.product(list_of_sites, repeat=2):
    correl_coef=scipy.stats.pearsonr(mean_log_abundance_dict[pair[0]],mean_log_abundance_dict[pair[1]])
    correl_list[i][j]=round(correl_coef[0],2)
    print("Correlation coefficient between ",pair[0]," and ",pair[1]," is ",str(round(correl_coef[0],2)))
    j+=1
    if j>len(list_of_sites)-1:
        j=0
        i+=1


# In[35]:


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

correl_list=np.array(correl_list)

fig, ax = plt.subplots(figsize=(10,10))
im = ax.imshow(1/correl_list,cmap='hot', interpolation='nearest')

# We want to show all ticks...
ax.set_xticks(np.arange(len(list_of_sites)))
ax.set_yticks(np.arange(len(list_of_sites)))
# ... and label them with the respective list entries
ax.set_xticklabels(list_of_sites)
ax.set_yticklabels(list_of_sites)


# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")


ax.set_title("Correlation between different sites")
fig.tight_layout()

plt.show()

