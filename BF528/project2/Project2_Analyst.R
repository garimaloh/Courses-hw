data <- read.table('gene_exp.diff',header=T,as.is=T)  # reading gene_exp.diff file into R
hist(data$log2.fold_change.,breaks=100,main = "Histogram of Log2 fold change for all genes",xlab = "Log2 fold change",col = "blue") # plotting histogram of log2.fold_change for all genes
data <- data[order(data$q_value),]        # rearranging data in order of q value
dim(data)#36329                     
dev.copy(pdf,'all_fold_change.pdf')       # saving the plot
dev.off()
head(data,n=10)

data.sig <- subset(data,significant=="yes")  # subsetting significant genes from all the genes
hist(data.sig$log2.fold_change.,breaks=100,main = "Histogram of Log2 fold change for significant DE genes",xlab = "Log2 fold change",col = "blue") # plotting histogram of log2.fold_change for differentially expressed genes
dev.copy(pdf,'sig_fold_change.pdf')          # saving the plot
dev.off()

data.sig <- data.sig[order(data.sig$q_value),]
data.sig.up <- subset(data.sig,log2.fold_change.>0) # subsetting upregulated genes
data.sig.dn <- subset(data.sig,log2.fold_change.<0) #  subsetting downregulated genes

dim(data.sig)#5193
dim(data.sig.up)#2760
dim(data.sig.dn)#2433
write(data.sig.up$gene,"upregulated_genes.csv") # saving to csv file
write(data.sig.dn$gene,"downregulated_genes.csv")# saving to csv file




