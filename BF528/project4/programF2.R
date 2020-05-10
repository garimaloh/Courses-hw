#loading packages
library(Seurat)
library(tximport)
library(dplyr)
library(EnsDb.Hsapiens.v86)
library(Matrix.utils)
library(SeqGSEA)
library(patchwork)
library(biomaRt)

#reading into file
files <- file.path('GSM2230760__salmon_quant')
file.exists(files)
txi<- tximport(files, type="alevin")

# no filtering
panc <- CreateSeuratObject(counts = txi$counts, project = "panc") 
#panc <- CreateSeuratObject(counts = txi_new$counts, project = "panc") 
print("no filtering")
panc

# filter out genes that are detected in less than 3 cells, and cells that are detected in less than 200 features
panc <- CreateSeuratObject(counts = txi$counts, project = "panc", min.cells = 3, min.features = 200)
print("filters: min.cells = 3, min.features = 200")
panc

# conversion to genenames
genes <- substr(panc@assays$RNA@counts@Dimnames[[1]], start = 1, stop = 15)
conversion <- convertEnsembl2Symbol(genes)
genes <- conversion$hgnc_symbol
panc@assays$RNA@counts@Dimnames[[1]] <- genes
panc@assays$RNA@data@Dimnames[[1]] <- genes

panc[["percent.mt"]] <- PercentageFeatureSet(panc, pattern = "^MT-")
panc <- subset(panc, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)
panc
VlnPlot(panc, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)
plot1 <- FeatureScatter(panc, feature1 = "nCount_RNA", feature2 = "percent.mt")
plot2 <- FeatureScatter(panc, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")
CombinePlots(plots = list(plot1, plot2))

panc <- subset(panc, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)
# report
print("filters: nFeature_RNA>200 and nFeature_RNA < 2500")
panc


# normalize counts matrix
panc <- NormalizeData(panc)
panc[["RNA"]]@meta.features <- data.frame(row.names = rownames(panc[["RNA"]]))
# filter out low variance genes; only include highly variable features (top 2000)
panc <- FindVariableFeatures(panc, selection.method = "vst", nfeatures = 2000)
# scale genes 
panc <- ScaleData(panc)
# report
print("normalized, filtered out low variable genes, scaled")
panc

top10 <- head(VariableFeatures(panc), 10)

# plot variable features with and without labels
plot1 <- VariableFeaturePlot(panc)
plot2 <- LabelPoints(plot = plot1, points = top10)
plot1 + plot2

needed_genes <- c("GCG", "INS", "SST", "PPY", "GHRL", "KRT19", "CPA1", "PDGFRB", "VWF", "PECAM1", "CD34", "CD163", "CD68", "IgG", "CD3", "CD8", "TPSAB1", "KIT", "CPA3")
print("the following genes are not in the filtered list:")
needed_genes[which(!needed_genes %in% panc@assays$RNA@counts@Dimnames[[1]])]

#PCA
panc <- RunPCA(panc, features = VariableFeatures(object = panc))
panc
VizDimLoadings(panc, dims = 1:2, reduction = "pca")
DimPlot(panc, reduction = "pca")
DimHeatmap(panc, dims = 1, cells = 500, balanced = TRUE)

panc <- JackStraw(panc, num.replicate = 100)
panc <- ScoreJackStraw(panc, dims = 1:20)
JackStrawPlot(panc, dims = 1:15)

ElbowPlot(panc)

panc <- RunUMAP(panc, dims = 1:10)
# note that you can set `label = TRUE` or use the LabelClusters function to help label
# individual clusters
DimPlot(panc, reduction = "umap")

panc <- FindNeighbors(panc, dims = 1:10)
panc <- FindClusters(panc, resolution = 0.5)
panc
head(Idents(panc), 5)
#cluster per cell
table ( Idents(panc) )


cluster_assignments <- Idents(panc)

head(Idents(panc), 5)
plot(cluster_assignments)

saveRDS(panc, file = "final.rds")
panc <- RunUMAP(panc, dims = 1:10)
Umap <- DimPlot(panc,label = TRUE, reduction = "umap",label.size = 6) 
Umap
