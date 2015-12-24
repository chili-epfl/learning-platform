library(plyr)
library("hydroGOF") #library for rmse
library("e1071") #library svm
library(ggplot2)

answerRadio<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/answers_radio.csv")
answerText<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/answers_text.csv")
answerBase<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/answer_base.csv")
question<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/questions.csv")
response<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/responses.csv")
test<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/tests.csv")
userAct<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/users_activities.csv")
activity<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/activity.csv")
user<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/users.csv")

#get a table of all answers with answer_id, question_id, body(the answer of the user), timestamp
anyAnswer<-rbind(answerRadio, answerText, deparse.level = 1)
colnames(anyAnswer)[1] <- "id"
allAnswers<-merge(anyAnswer,answerBase,by="id")
allAnswers<-allAnswers[with(allAnswers, order(question_id)), ]

#the answers concerning only the pre and post test
#Id taken from question table
preReqAnswer<-allAnswers[allAnswers$question_id %in% list("6","8","9","10","20","21"),]
preReqAnswer["points"] <- NA

#get the score for each answer
for( i in 1:nrow(preReqAnswer)){
  if(preReqAnswer$question_id[i] =="6"){
    if("0.1" %in% preReqAnswer$body[i]){
      preReqAnswer$points[i]<-1
    } else if ("-1" %in% preReqAnswer$body[i]){
      preReqAnswer$points[i]<-0
    } else {
      preReqAnswer$points[i]<-(-0.5)
    }
  }else if (preReqAnswer$question_id[i] =="8"){
    if("Transmissibility" %in% preReqAnswer$body[i]){
      preReqAnswer$points[i]<-1
    } else if ("I don't know" %in% preReqAnswer$body[i]){
      preReqAnswer$points[i]<-0
    } else {
      preReqAnswer$points[i]<-(-0.5)
    }
  
  } else if (preReqAnswer$question_id[i] =="9"){
    if(preReqAnswer$body[i] =="True"){
      preReqAnswer$points[i]<-1
    } else if (preReqAnswer$body[i]=="I don't know"){
      preReqAnswer$points[i]<-0
    } else {
      preReqAnswer$points[i]<-(-0.5)
    }
  } else if (preReqAnswer$question_id[i] =="10"){
    if(preReqAnswer$body[i] =="True"){
      preReqAnswer$points[i]<-1
    } else if (preReqAnswer$body[i]=="I don't know"){
      preReqAnswer$points[i]<-0
    } else {
      preReqAnswer$points[i]<-(-0.5)
    }
  } else if (preReqAnswer$question_id[i] =="20"){
      if("All" %in% preReqAnswer$body[i]){
        preReqAnswer$points[i]<-1
      } else if ("I don't" %in% preReqAnswer$body[i]){
        preReqAnswer$points[i]<-0
      } else {
        preReqAnswer$points[i]<-(-0.5)
      }
  } else {
    if("Diabetes" %in% preReqAnswer$body[i]){
      preReqAnswer$points[i]<-1
    } else if ("I don't" %in% preReqAnswer$body[i]){
      preReqAnswer$points[i]<-0
    } else {
      preReqAnswer$points[i]<-(-0.5)
    }
  } 
}



#calculate the result by response_id (by test taken by one user)
results <- ddply(preReqAnswer, .(response_id), summarise, total=sum(points) )
#add the user_id to results 
testUser<-response[c("id", "user_id")]
colnames(testUser)[1] <- "response_id"
results<-merge(results,testUser,by="response_id")

#get the time spend on tests and activities
timeInfo<-response[with(response, order(user_id,timestamp)), ]

#Data cleaning
#to get the timeline as 1:psycho test, 2:pretest 3:activity1, 4:activity2, 5:post test, 6: satisfaction survey
for( i in 1:(nrow(timeInfo)-1)){
#if two times 1 keep the second one
  if(timeInfo$test_id[i] =="1" & timeInfo$test_id[i]==timeInfo$test_id[i+1] & timeInfo$user_id[i]==timeInfo$user_id[i+1]){
    timeInfo<-timeInfo[-i,]
  }#assign to the pre-test id number 2  
  else if(timeInfo$test_id[i] =="3" & timeInfo$test_id[i]==timeInfo$test_id[i+1] & timeInfo$user_id[i]==timeInfo$user_id[i+1]){
    timeInfo$test_id[i]<-2
  } else if (timeInfo$test_id[i] =="4"){
    timeInfo$test_id[i]<-6
  }
}
#Assign 5 to post test
for( i in 1:(nrow(timeInfo))){
  if (timeInfo$test_id[i] =="3"){
    timeInfo$test_id[i]<-5
  }
}

for( i in 1:(nrow(userAct))){
  if (userAct$activity_id[i] =="1"){
    userAct$activity_id[i]<-3 
  } else if(userAct$activity_id[i] =="2"){
    userAct$activity_id[i]<-4
  }
}

#formatting userAct like timeInfo
userAct$id<-NULL
colnames(userAct)[3] <- "timestamp"
timeInfo$id<-NULL
colnames(timeInfo)[1] <- "activity_id"
timeInfo<-rbind(timeInfo, userAct, deparse.level = 1)

#time info will now contain all the activites that a user did with the timestamp from 1 to 6 if the activity completed
timeInfo<-timeInfo[with(timeInfo, order(user_id,activity_id)), ]

t<-timeInfo[timeInfo$activity_id == 2,] 
#120 psycho, 80 pretest, 104/167 act 1, 123 act 2, 111 posttest 78 satisfaction
#67  have gone through the psychological 
#94 that have done 5

#select only people that have done both activities=> we can show their learning gain
#user that has 2 and 5 
id5 = timeInfo[timeInfo$activity_id == 5,]$user_id
id2 = timeInfo[timeInfo$activity_id == 2,]$user_id
timeInfo<-timeInfo[timeInfo$user_id %in% id2 & timeInfo$user_id %in% id5 ,]

colnames(response)[1] <- "response_id"
response$user_id<-NULL
results<-merge(results,response,by="response_id")
results<-results[with(results, order(user_id,timestamp)), ]
#results now contain al the pre and post test with their scores 

#Calculate the learning gain
pt<-list()
pt$gain<-NA
pt$user_id<-NA

i<-1
while( i < (nrow(results)-1)){
  if(results$user_id[i]==results$user_id[i+1]){
    pt$gain[i]<-results$total[i+1]-results$total[i]
    pt$user_id[i]<- results$user_id[i]
    i<-i+2
  }
  else i<-i+1
}
gain_matrix=matrix(unlist(pt),length(pt[[1]]),length(pt));
colnames(gain_matrix)<-names(pt)
gain_matrix<-gain_matrix[complete.cases(gain_matrix),]

#add the age of the user to gain_matrix the data frame that will contain all the gathered features
colnames(user)[1]<-"user_id"
gain_matrix<-merge(gain_matrix, user, by="user_id")
gain_matrix$email<-NULL

#scale for questions with answers from 1 to 5 to get its scores
answer=list("Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree")
point=list(1,2,3,4,5)
scale=cbind(answer,point)

#get all the answers for consciousness questions 
consQ<-allAnswers[allAnswers$question_id %in% list("22","23","24","25","26"),]
consQ$points<-NA

#Some of the questions are positively keyed to consciousness so a good answer receives 
# a positive mark otherwise the answers receive a negative mark( 22+,23+,24+,25-,26-)
for( i in 1:(nrow(consQ)-1)){
  if(consQ$question_id[i] %in% list(22,23,24)){
    consQ$points[i]<- scale[scale[,1] %in% consQ$body[i]][[2]]
  } else {
    consQ$points[i]<- -(scale[scale[,1] %in% consQ$body[i]][[2]])
  }
}
resultsCons <- ddply(consQ, .(response_id), summarise, total=sum(points) )
#add the user_idto results 
resultsCons<-merge(resultsCons,testUser,by="response_id")
gain_matrix<-merge(resultsCons,gain_matrix, by="user_id")
colnames(gain_matrix)[3] <- "conscious"
gain_matrix$response_id<-NULL
gain_matrix<-gain_matrix[!duplicated(gain_matrix), ]

#assign the paths to each user in a table
paths<-read.csv("/Users/farahbouassida/Documents/MA3/semesterProject/users_activities.csv")
paths<-paths[with(paths, order(user_id,completed)), ]
paths<-paths[paths$user_id %in% id2 & paths$user_id %in% id5 ,]


gain_matrix$path<-NA
#paste(paths$activity_id[1],paths$activity_id[2])
for( i in 1:nrow(gain_matrix)){
  r<-paths[paths$user_id == gain_matrix$user_id[i] ,]$activity_id
  if(length(r)>=2)
    gain_matrix$path[i]<-r[1]*10+r[2]
  else 
    gain_matrix$path[i]<-NA
}
gain_matrix<-gain_matrix[complete.cases(gain_matrix),]



consciousness_plot<-ggplot(gain_matrix,aes(x=conscious,y=gain,colour=factor(path)))
consciousness_plot<-consciousness_plot+geom_point()
consciousness_plot<-consciousness_plot+geom_jitter()
consciousness_plot

plot<-ggplot(gain_matrix,aes(x=conscious,y=gain, fill=factor(path)))
plot<-plot + scale_fill_discrete(name="Learning\nPath",
                                 breaks=c("1 2", "1 4", "3 2","3 4"),
                                 labels=c("Video-Video", "Video-Text", "Text-Video","Text-Text"))
plot<-plot+geom_boxplot(outlier.colour = "green", outlier.size = 3)
plot
#Openess Questions
openQ<-allAnswers[allAnswers$question_id %in% list("30","31","32","33","34"),]
openQ$points<-NA
for( i in 1:(nrow(openQ)-1)){
  if(openQ$question_id[i] %in% list(30,31,32)){
    openQ$points[i]<- scale[scale[,1] %in% openQ$body[i]][[2]]
  } else {
    openQ$points[i]<- -(scale[scale[,1] %in% openQ$body[i]][[2]])
  }
}

resultsOpen <- ddply(openQ, .(response_id), summarise, open=sum(points) )
resultsOpen<-merge(resultsOpen,testUser,by="response_id")
resultsOpen$response_id<-NULL
gain_matrix<-merge(resultsOpen,gain_matrix, by="user_id") 


openness_plot<-ggplot(gain_matrix,aes(x=age,y=gain,colour=factor(path)))
openness_plot<-openness_plot+geom_point()
openness_plot<-openness_plot+geom_jitter()
openness_plot

#IQ questions
iqQ<-allAnswers[allAnswers$question_id %in% list("12","13"),]
iqQ$points<-NA
for( i in 1:nrow(iqQ)){
  if(iqQ$question_id[i] == "12"){
    if("Monday" == iqQ$body[i]){
      iqQ$points[i]<-1
    } else {
      iqQ$points[i]<-(-1)
    } 
  
  }else {
    if("12" == iqQ$body[i]){
      iqQ$points[i]<-1
    }  else {
      iqQ$points[i]<-(-1)
    }
  }
}

resultsIQ <- ddply(iqQ, .(response_id), summarise, QI=sum(points) )
resultsIQ<-merge(resultsIQ,testUser,by="response_id")
resultsIQ$response_id<-NULL
gain_matrix<-merge(resultsIQ,gain_matrix, by="user_id") 

qi_plot<-ggplot(gain_matrix,aes(x=IQ,y=gain,colour=factor(path)))
qi_plot<-qi_plot+geom_point()
qi_plot<-qi_plot+geom_jitter()

#GENDER 
gender<-allAnswers[allAnswers$question_id %in% list("35"),c("response_id","body")]
gender<-merge(gender,testUser, by="response_id")
gender$response_id<-NULL
colnames(gender)[1] <- "gender"
gain_matrix<-merge(gender,gain_matrix,by="user_id")
gender_plot<-ggplot(gain_matrix,aes(x=gender,y=gain,colour=factor(path)))
gender_plot<-gender_plot+geom_point()
gender_plot<-gender_plot+geom_jitter()
#Academic achieved level
#scale for questions with answers from 1 to 5
academic=list("Haven't graduated high school", "High school graduate", "Apprenticeship", "College student", "Bachelors", "Masters", "Doctorate" )
point=list(1,2,3,4,5,6,7)
scaleAcad=cbind(academic,point)
acadLevel<-allAnswers[allAnswers$question_id %in% list("36"),c("response_id","body")]
acadLevel$level<-NA
for( i in 1:nrow(acadLevel)){
  acadLevel$level[i]<- scaleAcad[scaleAcad[,1] %in% acadLevel$body[i]][[2]]

}
acadLevel$body<-NULL
acadLevel<-merge(acadLevel,testUser, by="response_id")
acadLevel$response_id<-NULL
gain_matrix<-merge(gain_matrix,acadLevel, buy="user_id")
#PaperFolding 
pfQ<-allAnswers[allAnswers$question_id %in% list("46","42","43","44","45"),c("response_id","body","question_id")]
pfQ$points<-NA
for( i in 1:nrow(pfQ)){
  if(pfQ$question_id[i] == "42"){
    if("A" == pfQ$body[i]){
      pfQ$points[i]<-1
    } else {
      pfQ$points[i]<-(-1)
    } 
    
  }else if(pfQ$question_id[i] == "43"){
    if("D" == pfQ$body[i]){
      pfQ$points[i]<-1
    }  else {
      pfQ$points[i]<-(-1)
    }
  }else if(pfQ$question_id[i] == "44"){
    if("B" == pfQ$body[i]){
      pfQ$points[i]<-1
    }  else {
      pfQ$points[i]<-(-1)
    }
  }else if(pfQ$question_id[i] == "45"){
    if("D" == pfQ$body[i]){
      pfQ$points[i]<-1
    }  else {
      pfQ$points[i]<-(-1)
    }
  }else if(pfQ$question_id[i] == "46"){
    if("B" == pfQ$body[i]){
      pfQ$points[i]<-1
    }  else {
      pfQ$points[i]<-(-1)
    }
  }
}

resultsPF <- ddply(pfQ, .(response_id), summarise, paperFolding=sum(points) )
resultsPF <- merge(resultsPF,testUser, by="response_id")
resultsPF$response_id<-NULL
gain_matrix<-merge(gain_matrix,resultsPF, by="user_id")

gain_matrix<-gain_matrix[!duplicated(gain_matrix), ]

pf_plot<-ggplot(gain_matrix,aes(x=t3,y=gain,colour=factor(path)))
pf_plot<-pf_plot+geom_point()
pf_plot<-pf_plot+geom_jitter()
pf_plot

plot<-ggplot(gain_matrix,aes(x=path,y=gain, fill=path))
plot<-plot + scale_fill_discrete(name="Learning\nPath",
                         breaks=c("1 2", "1 4", "3 2","3 4"),
                         labels=c("Video-Video", "Video-Text", "Text-Video","Text-Text"))
plot<-plot+geom_boxplot(outlier.colour = "green", outlier.size = 3)
plot 

p<-ggplot(gain_matrix,aes(x=factor(gender),y=gain,fill=factor(path))) 
p<-p+geom_boxplot(outlier.colour = "green", outlier.size = 3)
p<-p+scale_fill_discrete(name="Learning\nPath",
                    breaks=c("1 2", "1 4", "3 2","3 4"),
                    labels=c("Video-Video", "Video-Text", "Text-Video","Text-Text"))
p



#cor(as.numeric(gain_matrix$path), gain_matrix$gain)
for( i in 1:(nrow(timeInfo)-1)){
  #if two times 1 keep the second one
  if(timeInfo$activity_id[i]==timeInfo$activity_id[i+1] & timeInfo$user_id[i]==timeInfo$user_id[i+1]){
    timeInfo<-timeInfo[-i,]
  }
}

difftime(strptime(timeInfo$timestamp[3], "%Y-%m-%d %H:%M:%S"), strptime(timeInfo$timestamp[2], "%Y-%m-%d %H:%M:%S"), unit="secs")
gain_matrix$t1<-NA; gain_matrix$t2<-NA;gain_matrix$t3<-NA;gain_matrix$t4<-NA;
gain_matrix$t5<-NA; 
timeInfo$time<-NA

for( i in 1:nrow(gain_matrix)){
  time<-timeInfo[timeInfo$user_id == gain_matrix$user_id[i],]
  gain_matrix$timePretest[i]<-difftime(strptime(time[time$activity_id == 2,]$timestamp, "%Y-%m-%d %H:%M:%S"), strptime(time[time$activity_id == 1,]$timestamp, "%Y-%m-%d %H:%M:%S"), unit="secs")
  
} 
for( i in 1:nrow(gain_matrix)){
  time<-timeInfo[timeInfo$user_id == gain_matrix$user_id[i],]
  gain_matrix$timeAct1[i]<-difftime(strptime(time[time$activity_id == 3,]$timestamp, "%Y-%m-%d %H:%M:%S"), strptime(time[time$activity_id == 2,]$timestamp, "%Y-%m-%d %H:%M:%S"), unit="secs")
  
} 
for( i in 1:nrow(gain_matrix)){
  time<-timeInfo[timeInfo$user_id == gain_matrix$user_id[i],]
  gain_matrix$timeAct2[i]<-difftime(strptime(time[time$activity_id == 4,]$timestamp, "%Y-%m-%d %H:%M:%S"), strptime(time[time$activity_id == 3,]$timestamp, "%Y-%m-%d %H:%M:%S"), unit="secs")
  
} 

for( i in 1:nrow(gain_matrix)){
  time<-timeInfo[timeInfo$user_id == gain_matrix$user_id[i],]
  gain_matrix$timePosttest[i]<-difftime(strptime(time[time$activity_id == 5,]$timestamp, "%Y-%m-%d %H:%M:%S"), strptime(time[time$activity_id == 4,]$timestamp, "%Y-%m-%d %H:%M:%S"), unit="secs")
  
}

for( i in 1:nrow(gain_matrix)){
  gain_matrix$totalTime[i]<-gain_matrix$timePretest[i]+gain_matrix$timeAct1[i]+gain_matrix$timeAct2[i]+gain_matrix$timePosttest[i]
} 

gain_matrix$gender<-as.character(gain_matrix$gender)
gain_matrix$gender[gain_matrix$gender == gain_matrix$gender[1]] <- "0"
gain_matrix$gender[gain_matrix$gender != gain_matrix$gender[1]] <- "1"
gain_matrix<-gain_matrix[!duplicated(gain_matrix), ]

#guess gain given the path and the features

#first step is to scale the continuous variables
continuousVar<-gain_matrix[c("QI","open","conscious","paperFolding","timePretest","timeAct1","timeAct2","timePosttest","totalTime","gain","age")]
maxs<-apply(continuousVar,2,max)
mins<-apply(continuousVar,2,min)
scaled<-as.data.frame(scale(continuousVar,center=mins,scale=maxs-mins))
scaled$gender<-gain_matrix$gender
scaled$path<-gain_matrix$path
scaled$level<-gain_matrix$level


#3->4 text-text, 1->2 video-video
t<-scaled[scaled$path==12 | scaled$path==34,]
#boxplot
plot<-ggplot(t,aes(x=factor(open),y=gain, fill=factor(path)))
plot<-plot + scale_fill_discrete(name="Learning\nPath",
                                 breaks=c("1 2","3 4"),
                                 labels=c("Video-Video","Text-Text"))
plot<-plot+geom_boxplot(outlier.colour = "green", outlier.size = 3)
plot

#=============== scatter plot ==============
plot<-ggplot(t,aes(x=open,y=gain,colour=factor(path)))
plot<-plot+geom_point()
plot<-plot+geom_jitter()
plot



#cor(video$timeAct1,video$gain) = 0.4986121

#Quick scatterplot
scatterplot(gain ~ timePretest | path, data=t,xlab="IQ questions", ylab="Learning gain")

#Quick Boxplot 
boxplot(mpg~cyl,data=mtcars, main="Car Milage Data", xlab="Number of Cylinders",
        ylab="Miles Per Gallon")
#========================== Building Models ===========================
TT<-scaled[scaled$path == 34,] 
VV<-scaled[scaled$path == 12,]
VT<-scaled[scaled$path == 14,]
TV<-scaled[scaled$path == 32,]

rmse<-NA
data<-TT
data$gender<-as.factor(data$gender)
data$level<-as.factor(data$level)
data$path<-NULL
#rmse<-array(1:3, c(4,5)) to have bidemensionnal array
rmse<-NA
for(i in 1:5){
  index <- sample(1:nrow(dataVV),round(0.8*nrow(dataVV)))
  trainset <- dataVV[index,]
  testset <- dataVV[-index,]
  modelVV  <- svm(gain~., data = trainset, kernel = "radial")
  prediction <- predict(modelVV, testset[,-6])
  rmse[i]<-rmse(prediction,testset$gain)
}

#We try dummy encoding of level

IQ <- TT$QI
open<- TT$open
conscious<- TT$conscious
timePre<-TT$timePretest
timeAct1<-TT$timeAct1
timeAct2<- TT$timeAct2 
timePost<- TT$timePosttest
totalTime<-TT$totalTime
gender<-as.factor(TT$gender)
pf<-TT$paperFolding
level <- as.factor(TT$level)
gain<-TT$gain
age<-TT$age

xfactors <- model.matrix(TT$gain ~ level + gender)[,-1]
data <- as.matrix(data.frame(gain,age, IQ, open, conscious, timePre, timePost, timeAct1, timeAct2, totalTime, pf, xfactors))
data<-as.data.frame(data)

#now we try feature selection simply taken those who have correlation over 0.1 of correlation
highCorrTT<-TT[c("conscious","QI","open","timeAct2","timePosttest","gain")]
highCorrVV<-VV[c("conscious","QI" ,"open", "timeAct2", "timePosttest","gain")]
dataTT<-highCorrTT
dataTT$level<-as.factor(dataTT$level)
dataVV<-highCorrVV
dataVV$level<-as.factor(dataVV$level)
#***** To find the highly correlated features *****
#SVM with 5 highly correlated feat... 0.1412402
t1<-abs(cor(VV[,-10],TT$gain))
sort(t1, decreasing=TRUE)
View(t1)

#=======
#new regression with LASSO
library("glmnet")
data<-as.matrix(data)
index <- sample(1:nrow(data),round(0.8*nrow(data)))#0.7 is good proportion
trainset.x<-data[index,]
trainset.y<-gain[index]

testset.x <- data[-index,]
testset.y<-gain[-index]
#glmmod<-glmnet(trainset.x,y=trainset.y,alpha=0.5,family='gaussian')
for(i in 1:10){
  model<-cv.glmnet(trainset.x, trainset.y,family="gaussian")
  prediction<-predict(model, newx=testset.x, s=model$lambda.1se)
  rmse[i]<-rmse(prediction[,1],testset.y)
}

#============================================================


#mean(rmse)=0.1560314 with corr feature

#new regression with LASSO
IQ <- VV$QI
open<- VV$open
conscious<- VV$conscious
timePre<-VV$timePretest
timeAct1<-VV$timeAct1
timeAct2<- VV$timeAct2 
timePost<- VV$timePosttest
totalTime<-VV$totalTime
gender<-as.factor(VV$gender)
pf<-VV$paperFolding
level <- as.factor(VV$level)
gain<-VV$gain
age<-VV$age

xfactors <- model.matrix(VV$gain ~ level + gender)[,-1]
dataVV <- as.matrix(data.frame(gain,age, IQ, open, conscious, timePre, timePost, timeAct1, timeAct2, totalTime, pf, xfactors))

index <- sample(1:nrow(dataVV),round(0.8*nrow(dataVV)))#0.7 is good proportion
trainset.x<-dataVV[index,]
trainset.x<-trainset.x[,-1]
trainset.y<-gain[index]

testset.x <- dataVV[-index,]
testset.x<-testset.x[,-1]
testset.y<-gain[-index]
#glmmod<-glmnet(trainset.x,y=trainset.y,alpha=0.5,family='gaussian')
for(i in 1:10){
  modelVV<-cv.glmnet(trainset.x, trainset.y,family="gaussian")
  predictionVV<-predict(modelVV, newx=testset.x, s=modelVV$lambda.1se)
  rmse[i]<-rmse(predictionVV[,1],testset.y)
}


#================ Comparison ==================
TTwithVV<-dataVV[,1:5]
VVwithTT<-dataTT[,1:5]
predTTwithVV<-predict(modelVV,TTwithVV)
TTwithVV$gain<-predTTwithVV
TTwithVV$path<-"VV"
predVVwithTT<-predict(modelTT,VVwithTT)
VVwithTT$gain<-predVVwithTT
VVwithTT$path<-"TT"


#add gain to both 
res<-dataTT
j<-0
for(i in 1:nrow(res)){
  if(res$gain[i]<TTwithVV$gain[i]){
    #res[i,]<-TTwithVV[i,]
    j<-j+1
  } 
}

res2<-dataVV
for(i in 1:nrow(res)){
  if(res2$gain[i]<VVwithTT$gain[i]){
    res2[i,]<-TTwithVV[i,]
  } 
}

dataVV$path<-"VV"
TTwithVV<-dataVV[,1:5]
predTTwithVV<-predict(modelVV,dataTT[,-7])
plot<-ggplot(res2,aes(x=open,y=timeAct2,colour=factor(path)))
plot<-plot+geom_point()
plot<-plot+geom_jitter()
plot<-plot+ylim(0,0.05)
plot