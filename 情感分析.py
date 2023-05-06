import jieba
import pandas as pd

# 停用词典过滤
stop_words = []
with open('G:/00毕业论文/3 情感分析/词典/SnowNLP停用词.txt','r',encoding='utf-8') as f:
	for word in f:
		stop_words.append(word.strip()) # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。

# 读取否定词文件
negative_words = []
with open('G:/00毕业论文/3 情感分析/词典/否定词.txt','r',encoding='utf-8') as f:
	for word in f:
		negative_words.append(word.strip())

# 读取程度副词文件
degree_words = []
with open('G:/00毕业论文/3 情感分析/词典/程度副词.txt','r',encoding='utf-8') as f:
	for word in f:
		degree_words.append(word.rstrip(",2"))

# 生成新的停用词表
stop_words_new = []
for word in stop_words:
	if(word not in negative_words) and (word not in degree_words):
		stop_words_new.append(word)

# jieba分词后去除停用词
def seg_word(sentence):
	# jieba.setLogLevel(jieba.logging.INFO)
	seg_list = jieba.cut(sentence)
	seg_result = []
	for i in seg_list:
		seg_result.append(i)
	# 去除停用词
	return list(filter(lambda x :x not in stop_words_new,seg_result))

# 找出文本中的情感词、否定词和程度副词
def classify_words(word_list):
	# 读取情感词典文件
	with open('G:/00毕业论文/3 情感分析/词典/Jiang20Yao21_media_sentiment_score.txt', 'r+', encoding='utf-8') as f:
		emo_list = f.readlines()
		emo_dict = {}     # 创建情感字典
		# 读取词典每一行的内容，将其转换成字典对象，key为情感词，value为其对应的权重
		for i in emo_list:
			if len(i.split(' ')) == 2:
				emo_dict[i.split(' ')[0]] = i.split(' ')[1]

	# 读取否定词文件
	with open('G:/00毕业论文/3 情感分析/词典/否定词.txt', 'r+', encoding='utf-8') as f:
		negative_words = f.readlines()

	# 读取程度副词文件
	with open('G:/00毕业论文/3 情感分析/词典/程度副词.txt', 'r+', encoding='utf-8') as f:
		degree_list = f.readlines()
		degree_dict = {}
		for i in degree_list:
			degree_dict[i.split(',')[0]] = i.split(',')[1]

	emo_word = {}
	negative_word = {}
	degree_word = {}
	# 分类
	for i in range(len(word_list)):
		word = word_list[i]
		if (word in emo_dict.keys()) and (word not in negative_words) and (word not in degree_dict.keys()):
			#找出分词结果中在情感字典中的词
			emo_word[i] = emo_dict[word].strip()
		elif (word in negative_words) and (word not in degree_dict.keys()):
			#分词结果中在否定词列表中的词
			negative_word[i] = -1
		elif word in degree_dict.keys():
			#分词结果中在程度副词中的词
			degree_word[i] = degree_dict[word]
	return emo_word,negative_word,degree_word

# 计算情感词的分数
def score_emotion(emo_word,negative_word,degree_word,seg_result):
	# 权重初始化为1
	W = 1
	score = 0
	# 情感词下标初始化
	emotion_index = -1
	# 情感词的位置下标集合
	emotion_index_list = list(emo_word.keys())
	# 遍历分词结果
	for i in range(0,len(seg_result)):
		# 如果是情感词
		if i in emo_word.keys():
			# 权重*情感词得分
			score += W * float(emo_word[i])
			# 情感词下标加一，获取下一个情感词的位置
			emotion_index += 1
			if emotion_index < len(emotion_index_list)-1:
				# 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
				for j in range(emotion_index_list[emotion_index],emotion_index_list[emotion_index+1]):
					# 更新权重，如果有否定词，权重取反
					if j in negative_word.keys():
						W *= -1
					elif j in degree_word.keys():
						W *= float(degree_word[j])
		# 定位到下一个情感词
		if emotion_index < len(emotion_index_list) - 1:
			i = emotion_index_list[emotion_index + 1]
	return score

# 计算得分
def emotion_score(sentence):
	# 1.对文档分词
	seg_list = seg_word(sentence)
	# 2.将分词结果转换成字典，找出情感词、否定词和程度副词
	emo_word,negative_word,degree_word = classify_words(seg_list)
	# 3.计算得分
	score = score_emotion(emo_word,negative_word,degree_word,seg_list)
	return score

if __name__ == '__main__':
	# 读取待分析文本数据
	data = pd.read_csv('G:/00毕业论文/2 数据/螺纹钢.csv').astype(str)
	print("数据已读取！")
	sentence = data.title

	# 导出分词和情感分值
	data['cut_comment'] = sentence.transform(seg_word)
	print("分词已完成！")
	data['sentiment_score'] = sentence.transform(emotion_score)
	print("情感分析已完成！")
	data.to_excel("sentiment_result_002235.xlsx",index=False)
	print("数据已导出！")