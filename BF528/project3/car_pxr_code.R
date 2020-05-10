ds1<- read.csv("sample2.csv",sep=',')

head (ds1)

ds1<- ds1[!colnames(ds1)%in%ds2_col]
ds2<- read.csv("control_counts_m.csv",sep=',')
ds2_col <- colnames(ds2)
ds2_col <- ds2_col[ds2_col!='Geneid']
total<-merge(ds1,ds2,by="Geneid")
head(total)

library(DESeq2)
# load counts
cnts <- total
# filter out rows that have any zeros for funzies
cnts <- subset(cnts,rowSums(cnts==0)==0)
# sample information
info <- read.csv("toxgroup_1_rna_infos2.csv")
info_col <- as.vector(info['Run'])
#Filter counts by sample names from meta data file
row.names(cnts) <- cnts[,1]
cnts <- cnts[,-1]
cnts_filter <- cnts
cnts_filter <- apply(cnts_filter,1:2,round)
rownames(info) <- info$Run
# Check for Gene IDS
all(row.names(info) %in% colnames(cnts_filter))
all(row.names(info) == colnames(cnts_filter))
info_row <- intersect(rownames(info),colnames(cnts_filter))
cnts_filter <- subset.matrix(cnts_filter,select = info_row)
# create the DESeq object
dds <- DESeqDataSetFromMatrix(
  countData = cnts_filter,
  colData = info,
  design= ~ mode_of_action
)
# relevel mode_of_action as factor
dds$mode_of_action <- relevel(dds$mode_of_action, ref='Control')
# run DESeq
dds <- DESeq(dds)
res <- results(dds, contrast=c('mode_of_action','CAR.PXR','Control'))
res <- lfcShrink(dds, coef=2)
# write out DE results
write.csv(res,'deseq_results_car.csv')
# write out matrix of normalized counts
write.csv(counts(dds,normalized=TRUE),'deseq_norm_counts_car.csv')
#ds3<-read.csv("deseq_results.csv",sep=',')
res[order(res$padj),]

sigDE <- subset(res,padj <0.05)

sigDE <-head(sigDE,n=100)
write.csv(sigDE,'top100_car_pxr.csv')
dim(sigDE)

hist(sigDE$log2FoldChange,breaks=100,col="blue",main="Car/Pxr",xlab="log2FoldChange")

plot(-log(res$pvalue)~res$log2FoldChange,pch=20,col="red")

#volcano plot

library(EnhancedVolcano)

EnhancedVolcano(res,
                lab = rownames(res),
                x = 'log2FoldChange',
                y = 'padj',
                xlim = c(-5, 8) ,pointSize=2,
                 widthConnectors = 0.5)

     