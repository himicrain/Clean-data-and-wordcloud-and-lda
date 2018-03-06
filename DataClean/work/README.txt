这几个文件都用到了utils.py和Clean.py文件，这几个文件不能修改，

Sign 分隔符只需要在utils里配置就行，csv文件必须放在csv目录下，

运行后，会自动生成clean目录，该目录下会生成一个str.txt文件，
str.txt文件是csv文件 preprocess 后生成的，

需要安装的包有 sklearn numpy networkx textblob wordcloud