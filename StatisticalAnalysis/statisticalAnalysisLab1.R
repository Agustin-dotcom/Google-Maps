rm(list=ls())

source("C:/Users/Agus/OneDrive - Universidad de Castilla-La Mancha/Escritorio/2do año/2do cuatri/Statistics (Fernando)/R/Libraries/getMe.libraries.R")
getMe.libraries()
install.packages("RSQLite")
library(RSQLite)

# Especifica la ruta a tu archivo .db
db_path <- "C:\\googleMapsVS\\Google-Maps\\resultados_programa.db"

# Conéctate a la base de datos
conn <- dbConnect(SQLite(), dbname = db_path)

# Lista las tablas en la base de datos
tables <- dbListTables(conn)
print(tables)

# Lee una tabla específica en un data frame
df <- dbReadTable(conn, "resultados")
print(head(df))

# Cierra la conexión
dbDisconnect(conn)
DATA <- df
nrow(DATA)
summary(DATA)

DATA$typeOfProblem <- factor(DATA$typeOfProblem)

DATA$algorithm <- factor(DATA$algorithm)
summary(DATA)

library(ggplot2)
ggplot(DATA, aes(y = executionTime, fill = algorithm))+
  geom_boxplot(alpha = 0.7)+
  ylim(0,0.015)
.desc.numeric(DATA$executionTime)$min
DATA[DATA$executionTime <0,]


summary(DATA)

ggplot(DATA,aes(x = DATA$SolutionCost, fill = DATA$algorithm))+
  geom_density(alpha = 0.7)+
  xlim(0,2000)

ggplot(DATA,aes(y=DATA$SolutionCost, fill = DATA$algorithm))+
  geom_boxplot(alpha = 0.8)+
  ylim(0,1000)

ggplot(DATA,aes(x = typeOfProblem,y=SolutionCost,fill = algorithm))+
  geom_bar(stat = "identity",position = "dodge",alpha = 0.8)

summary(DATA)
.desc.numeric(DATA$executionTime,DATA$algorithm)

ggplot(DATA,aes(y = typeOfProblem, y = executionTime, fill = algorithm))+
  geom_boxplot(stat = "identity", position = "dodge")

ggplot(DATA,aes(x = nodesGenerated,fill = algorithm))+
  geom_density(alpha = 0.7)+
xlim(0,10000)

View(DATA)
nameIWant <- names(table(DATA$algorithm))[2]
nameIWantNow <- names(table(DATA$algorithm))[1]
nowIWantThisName <- names(table(DATA$algorithm))[2]
DATA[DATA$algorithm == nameIWant,]
DATA[DATA$algorithm == nameIWantNow,]
DATA[DATA$algorithm == nowIWantThisName,]
DATA[DATA$nameProblem == "calle_cardenal_tabera_y_araoz_albacete_2000_1.json",]

DATA[DATA$nameProblem =="plaza_isabel_ii_albacete_250_0.json",]

DATA[DATA$nameProblem =="calle_herreros_albacete_2000_2.json",]
