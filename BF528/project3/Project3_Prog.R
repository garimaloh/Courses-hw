library("edgeR")
library("magrittr")
library("stringr")
#args <- commandArgs(trailingOnly = TRUE)
#stopifnot(length(args) > 0, file.exists(args))
#f_counts <- args
# For testing:

f_counts <- Sys.glob("SRR*txt")

raw <- readDGE(f_counts, columns = c(1,7), comment.char = "#",header=TRUE)
counts <- as.matrix(raw)

# Change column names from filenames to sample names ------------------------

#names(dimnames(counts)) <- c("Gene_id", "")
counts=data.frame(counts)

counts=cbind(rownames(counts),counts)
colnames(counts)[1]="Gene_id"
rownames(counts)=NULL

counts <- counts[order(rownames(counts)), order(as.numeric(colnames(counts)))]


# Write to standard out --------------------------------------------------------
# head(counts)
write.csv(counts, file = "countsfinal.csv", quote = TRUE,row.names=FALSE)

counts.nozero=counts[which (rowSums(counts[,-1])>0),]

write.csv(counts.nozero, file = "counts_nonzero.csv", quote = TRUE,row.names=FALSE)
par(mar=c(7,8,4,4))
colors = c(rep("red",3),rep("blue",3),rep("green",4))
logcounts <- cpm(counts.nozero,log=TRUE)
boxplot(log2(counts.nozero[,-1]),las=2,col=colors() ,frame.plot = FALSE,ylab="log2(counts)")
abline(h=7.5,col="blue")
dev.copy(png,'boxplot.png')
dev.off()