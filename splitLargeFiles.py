#split large files so they are smaller than 100mb (github constraint)
### LSA

lsaFile = open("COCA_newspaper_magazine_export_LSA.csv").read().split("\n")
len(lsaFile)/4

lsaFileSmalla = lsaFile[:10000]
lsaFileSmallb = lsaFile[10000:20000]
lsaFileSmallc = lsaFile[20000:30000]
lsaFileSmalld = lsaFile[30000:40000]
lsaFileSmalle = lsaFile[40000:]

def writePart(l,name):
	outf = open(name,"w")
	outf.write("\n".join(l))
	outf.flush()
	outf.close()

writePart(lsaFileSmalla,"COCA_newspaper_magazine_export_LSA_Small_A.csv")
writePart(lsaFileSmallb,"COCA_newspaper_magazine_export_LSA_Small_B.csv")
writePart(lsaFileSmallc,"COCA_newspaper_magazine_export_LSA_Small_C.csv")
writePart(lsaFileSmalld,"COCA_newspaper_magazine_export_LSA_Small_D.csv")
writePart(lsaFileSmalle,"COCA_newspaper_magazine_export_LSA_Small_E.csv")

### word2vec
word2vecFile = open("COCA_newspaper_magazine_export_word2vec.csv").read().split("\n")
len(word2vecFile)

word2vecFileSmalla = word2vecFile[:10000]
word2vecFileSmallb = word2vecFile[10000:20000]
word2vecFileSmallc = word2vecFile[20000:30000]
word2vecFileSmalld = word2vecFile[30000:40000]
word2vecFileSmalle = word2vecFile[40000:]

writePart(word2vecFileSmalla,"COCA_newspaper_magazine_export_word2vec_Small_A.csv")
writePart(word2vecFileSmallb,"COCA_newspaper_magazine_export_word2vec_Small_B.csv")
writePart(word2vecFileSmallc,"COCA_newspaper_magazine_export_word2vec_Small_C.csv")
writePart(word2vecFileSmalld,"COCA_newspaper_magazine_export_word2vec_Small_D.csv")
writePart(word2vecFileSmalle,"COCA_newspaper_magazine_export_word2vec_Small_E.csv")
