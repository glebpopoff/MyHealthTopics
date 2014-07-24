healthTopicImageMap = {
'asthma':'/static/images/topics/asthma.png',
'attention deficit hyperactivity disorder':'/static/images/topics/adhd.png',
'adhd':'/static/images/topics/adhd.png',
'add':'/static/images/topics/adhd.png',
'hiv/aids':'/static/images/topics/aids.png',
'hiv':'/static/images/topics/aids.png',
'ids':'/static/images/topics/aids.png',
'allergy':'/static/images/topics/allergies.png',
'alzheimer\'s disease':'/static/images/topics/AlzheimersDisease.png',
'alzheimer\'s':'/static/images/topics/AlzheimersDisease.png',
'alzheimer':'/static/images/topics/AlzheimersDisease.png',
'anxiety':'/static/images/topics/Anxiety.png',
'arthritis':'/static/images/topics/Arthritis.png',
'breast cancer':'/static/images/topics/breastcancer.png',
'chronic fatigue syndrome':'/static/images/topics/cfs.png',
'crohn&apos;s disease':'/static/images/topics/crohnsdisease.png',
'chronic fatigue syndrome':'/static/images/topics/cfs.png',
'cfs':'/static/images/topics/cfs.png',
'cystic fibrosis':'/static/images/topics/CysticFibrosis.png',
'cystic':'/static/images/topics/CysticFibrosis.png',
'fibrosis':'/static/images/topics/CysticFibrosis.png',
'depression':'/static/images/topics/depression.png',
'diabetes':'/static/images/topics/diabetes.png',
'epilepsy':'/static/images/topics/epilepsy.png',
'fibromyalgia':'/static/images/topics/fibromyalgia.png',
'gerd':'/static/images/topics/gerd.png',
'heartburn':'/static/images/topics/heartburn.png',
'headache':'/static/images/topics/headache.png',
'migrain':'/static/images/topics/headache.png',
'heart decease':'/static/images/topics/HeartAttack.png',
'heart':'/static/images/topics/HeartAttack.png',
'heart attack':'/static/images/topics/HeartAttack.png',
'hepatitis':'/static/images/topics/hepatitis.png',
'irritable bowel syndrome':'/static/images/topics/ibs.png',
'irritable bowel':'/static/images/topics/ibs.png',
'ibs':'/static/images/topics/ibs.png',
'lupus':'/static/images/topics/lupus.png',
'lyme disease':'/static/images/topics/lyme-disease.png',
'lyme':'/static/images/topics/lyme-disease.png',
'parkinson\'s disease':'/static/images/topics/parkinsons.png',
'parkinson\'s':'/static/images/topics/parkinsons.png',
'parkinson':'/static/images/topics/parkinsons.png',
'prostate':'/static/images/topics/prostate-cancer.png',
'prostate cancer':'/static/images/topics/prostate-cancer.png'
}

def get_health_topic_image(topic):
	topic = topic.lower()
	if (topic in healthTopicImageMap):
		return healthTopicImageMap[topic]
	else:
		return ''