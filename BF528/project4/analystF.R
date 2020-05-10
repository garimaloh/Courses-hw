library(dplyr)
library(Seurat)
library(patchwork)
library(dplyr)
library(Seurat)
#reading Rcells file into R
cells <- readRDS("GSM2230760_seurat.rda")
#cells<-readRDS("final.rds")
#Identify marker genes for each cluster
cells.markers <- FindAllMarkers(cells, only.pos = TRUE, min.pct = 0.25, 
                                logfc.threshold = 0.25)
write.csv(cells.markers,"cellmarker.csv")
#Label clusters as a cell type based on marker genes.
#used author supplementry sheet and Pangloadb to identify cell types according to marker genes
#Visualize the clustered cells using a projection method.


new.cluster.ids <- c("Delta", "Beta", "Alpha", "Acinar", "Alpha","Ductal", "Beta", 
                       "Cytotoxic T", "Alpha"," Stellate",
                      "Ductal","Acinar", "Mast")
Umap <- DimPlot(cells, reduction = "umap", label = TRUE,label.size=6) 
Umap

names(new.cluster.ids) <- levels(cells)
cells1 <- RenameIdents(cells, new.cluster.ids)
Umap <- DimPlot(cells1, reduction = "umap", label = TRUE,label.size=6) 
Umap

#Visualize the top marker genes per cluster
top2 <- cells.markers %>% group_by(cluster) %>% top_n(n = 2, wt = avg_logFC)
top10 <- cells.markers %>% group_by(cluster) %>% top_n(n = 10, wt = avg_logFC)
cluster0.marker <- top5[top5$cluster==0,]
cluster1.marker <- top5[top5$cluster==1,]
cluster2.marker <- top5[top5$cluster==2,]
cluster3.marker <- top5[top5$cluster==3,]
cluster4.marker <- top5[top5$cluster==4,]
cluster5.marker <- top5[top5$cluster==5,]
cluster6.marker <- top5[top5$cluster==6,]
cluster7.marker <- top5[top5$cluster==7,]
cluster8.marker <- top5[top5$cluster==8,]
cluster9.marker <- top5[top5$cluster==9,]
cluster10.marker <- top5[top5$cluster==10,]
cluster11.marker <- top5[top5$cluster==11,]
cluster12.marker <- top5[top5$cluster==12,]
DoHeatmap(cells1, features = top2$gene,angle = 90) 
write.csv(top2,"top2marker.csv")
#marlene type plot
FeaturePlot(cells, features = c("SP100","INS","FN1","REG1B","TTR","KRT19","EEF1A2","ACER3","GC"))

VlnPlot(cells, features = c("GCG"))                                
FeaturePlot(cells, features = c("COL1A1","CRP","ALDOB","ACP5"))


#Find novel marker genes
feature0.markers <- FindMarkers(cells, ident.1 = "0", ident.2 = NULL, only.pos = TRUE)
feature0=feature0.markers[which(feature0.markers$p_val_adj<0.05),]
#marker genes that already exist
marker0=cells.markers[which(cells.markers$cluster==0),]
marker0=marker0$gene
#drop marker genes that exist
f0=feature0[-which(row.names(feature0) %in% marker0),]

feature1.markers <- FindMarkers(cells, ident.1 = "1", ident.2 = NULL, only.pos = TRUE)
feature1=feature1.markers[which(feature1.markers$p_val_adj<0.05),]
marker1=cells.markers[which(cells.markers$cluster==1),]
marker1=marker1$gene
f1=feature1[-which(row.names(feature1) %in% marker1),]

feature2.markers <- FindMarkers(cells, ident.1 = "2", ident.2 = NULL, only.pos = TRUE)
feature2=feature2.markers[which(feature2.markers$p_val_adj<0.05),]
marker2=cells.markers[which(cells.markers$cluster==2),]
marker2=marker2$gene
f2=feature2[-which(row.names(feature2) %in% marker2),]

feature3.markers <- FindMarkers(cells, ident.1 = "3", ident.2 = NULL, only.pos = TRUE)
feature3=feature3.markers[which(feature3.markers$p_val_adj<0.05),]
marker3=cells.markers[which(cells.markers$cluster==3),]
f3=feature3[-which(row.names(feature3) %in% marker3$gene),]

feature4.markers <- FindMarkers(cells, ident.1 = "4", ident.2 = NULL, only.pos = TRUE)
feature4=feature4.markers[which(feature4.markers$p_val_adj<0.05),]
marker4=cells.markers[which(cells.markers$cluster==4),]
f4=feature4[-which(row.names(feature4) %in% marker4$gene),]

feature5.markers <- FindMarkers(cells, ident.1 = "5", ident.2 = NULL, only.pos = TRUE)
feature5=feature5.markers[which(feature5.markers$p_val_adj<0.05),]
marker5=cells.markers[which(cells.markers$cluster==5),]
f5=feature5[-which(row.names(feature5) %in% marker5$gene),]

feature6.markers <- FindMarkers(cells, ident.1 = "6", ident.2 = NULL, only.pos = TRUE)
feature6=feature6.markers[which(feature6.markers$p_val_adj<0.05),]
marker6=cells.markers[which(cells.markers$cluster==6),]
f6=feature6[-which(row.names(feature6) %in% marker6$gene),]

feature.markers <- FindMarkers(cells, ident.1 = "7", ident.2 = NULL, only.pos = TRUE)
feature=feature.markers[which(feature.markers$p_val_adj<0.05),]
marker=cells.markers[which(cells.markers$cluster==7),]
f7=feature[-which(row.names(feature) %in% marker$gene),]

feature.markers <- FindMarkers(cells, ident.1 = "8", ident.2 = NULL, only.pos = TRUE)
feature=feature.markers[which(feature.markers$p_val_adj<0.05),]
marker=cells.markers[which(cells.markers$cluster==8),]
f8=feature[-which(row.names(feature) %in% marker$gene),]

feature.markers <- FindMarkers(cells, ident.1 = "9", ident.2 = NULL, only.pos = TRUE)
feature=feature.markers[which(feature.markers$p_val_adj<0.05),]
marker=cells.markers[which(cells.markers$cluster==9),]
f9=feature[-which(row.names(feature) %in% marker$gene),]

feature.markers <- FindMarkers(cells, ident.1 = "10", ident.2 = NULL, only.pos = TRUE)
feature=feature.markers[which(feature.markers$p_val_adj<0.05),]
marker=cells.markers[which(cells.markers$cluster==10),]
f10=feature[-which(row.names(feature) %in% marker$gene),]

feature.markers <- FindMarkers(cells, ident.1 = "11", ident.2 = NULL, only.pos = TRUE)
feature=feature.markers[which(feature.markers$p_val_adj<0.05),]
marker=cells.markers[which(cells.markers$cluster==11),]
f11=feature[-which(row.names(feature) %in% marker$gene),]

feature.markers <- FindMarkers(cells, ident.1 = "12", ident.2 = NULL, only.pos = TRUE)
feature=feature.markers[which(feature.markers$p_val_adj<0.05),]
marker=cells.markers[which(cells.markers$cluster==12),]
f12=feature[-which(row.names(feature) %in% marker$gene),]

f0$cluster=rep(0,length(f0$p_val))
f1$cluster=rep(1,length(f1$p_val))
f2$cluster=rep(2,length(f2$p_val))
f3$cluster=rep(3,length(f3$p_val))
f4$cluster=rep(4,length(f4$p_val))
f5$cluster=rep(5,length(f5$p_val))
f6$cluster=rep(6,length(f6$p_val))
f7$cluster=rep(7,length(f7$p_val))
f8$cluster=rep(8,length(f8$p_val))
f9$cluster=rep(9,length(f9$p_val))
f10$cluster=rep(10,length(f10$p_val))
f11$cluster=rep(11,length(f11$p_val))
f12$cluster=rep(12,length(f12$p_val))

novel_markers=rbind(f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12)
write.csv(novel_markers,'novel_markers.csv')

FeaturePlot(cells, features = c("PHACTR1","G6PC2","COL1A2","PLA2G1B","IRX2","KRT7","APOBEC2","SLC25A51P4","AL606807.1"))

FeaturePlot(cells, features = c("CRLF1","EPHA2","AC008760.2","FYB1"))