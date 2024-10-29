rm(list=ls())

source("C:/Users/Agus/OneDrive - Universidad de Castilla-La Mancha/Escritorio/2do año/2do cuatri/Statistics (Fernando)/R/Libraries/getMe.libraries.R")
getMe.libraries()
#install.packages("RSQLite")
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

ggplot(DATA,aes(x = SolutionCost, fill = algorithm))+
  geom_density(alpha = 0.7)+
  xlim(0,2000)

ggplot(DATA,aes(y=SolutionCost, fill = algorithm))+
  geom_boxplot(alpha = 0.8)+
  ylim(0,1000)

ggplot(DATA,aes(x = typeOfProblem,y=SolutionCost,fill = algorithm))+
  scale_fill_viridis(discrete = TRUE) +
  geom_bar(stat = "identity",position = "dodge",alpha = 0.8)

summary(DATA)
.desc.numeric(DATA$executionTime,DATA$algorithm)

ggplot(DATA,aes(x = typeOfProblem,y = nodesGenerated, fill = algorithm))+
  geom_bar(stat = "identity", position = "dodge")

ggplot(DATA,aes(x = typeOfProblem,y = nodesExpanded, fill = algorithm))+
  geom_bar(stat = "identity", position = "dodge")

ggplot(DATA,aes(x = nodesGenerated,fill = algorithm))+
  geom_density(alpha = 0.7)+
xlim(0,2500)
library(ggplot2)
library(viridis)

ggplot(DATA, aes(x = nodesGenerated, fill = algorithm)) +
  geom_density(alpha = 0.7) +
  scale_fill_viridis(discrete = TRUE) +
  xlim(0, 2500)
library(ggplot2)
library(RColorBrewer)

ggplot(DATA, aes(x = nodesGenerated, fill = algorithm)) +
  geom_density(alpha = 0.7) +
  scale_fill_brewer(palette = "Set1") +
  xlim(0, 2500)
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
View(DATA)
DATA[DATA$nameProblem =="calle_herreros_albacete_2000_2.json",]


# x --> nameProblem, strategy
# y --> nodesGenerated

library(ggplot2)
ggplot(DATA,aes(x = nodesGenerated, fill = algorithm))+
  geom_density(alpha = 0.7)+
  xlim(0,1500)

ggplot(DATA,aes(y = nodesGenerated, fill = algorithm))+
  geom_boxplot(alpha = 0.7)+
  ylim(0,200)

#ggplot(DATA,aes(x = (nameProblem,DATA$algorithm), y = nodesGenerated))+
#  geom_line(alpha = 0.7)


library(dplyr)
library(tidyverse)
library(ggrepel)
library(ggtext)

library(showtext)
font_add_google("Lato")
showtext_auto()
DATA <- DATA %>% 
  # Extract year
  #mutate(year = lubridate::year(date)) %>% 
  # Subset variables
  select(nameProblem, algorithm, nodesGenerated) %>% 
  # If there is more than one record per year/country, use the mean 
  group_by(nameProblem, algorithm) %>% 
  #summarize(price = mean(dollar_price)) %>% 
  # Keep countries/regions with records for the last 21 years  
  # (from 2000 to 2020 inclusive)
  #group_by(iso_a3) %>% 
  #filter(n() == 21)

# Also define the group of countries that are going to be highlighted
highlights <- names(table(DATA$algorithm))
n <- length(highlights)

#countries <- df_mac %>% 
#  filter(year == 2008) %>% 
 # pull(iso_a3)

#df_mac_indexed_2008 <- df_mac %>% 
  # Keep countries that have a record for 2008, the index year.
 # group_by(iso_a3) %>%
  #filter(iso_a3 %in% countries) %>% 
  # Compute the `price_index`
  # mutate(
  #   ref_year = 2008,
  #   price_index = price[which(year == 2008)],
  #   price_rel = price - price_index,
  #   # Create 'group', used to color the lines.
  #   group = if_else(iso_a3 %in% highlights, iso_a3, "other"),
  #   group = as.factor(group)
  # ) %>% 
  # mutate(
  #   group = fct_relevel(group, "other", after = Inf),
  #   name_lab = if_else(year == 2020, name, NA_character_)
  # ) %>% 
  # ungroup()
# This theme extends the 'theme_minimal' that comes with ggplot2.
# The "Lato" font is used as the base font. This is similar
# to the original font in Cedric's work, Avenir Next Condensed.
theme_set(theme_minimal(base_family = "Lato"))


theme_update(
  # Remove title for both x and y axes
  axis.title = element_blank(),
  # Axes labels are grey
  axis.text = element_text(color = "grey40"),
  # The size of the axes labels are different for x and y.
  axis.text.x = element_text(size = 20, margin = margin(t = 5)),
  axis.text.y = element_text(size = 17, margin = margin(r = 5)),
  # Also, the ticks have a very light grey color
  axis.ticks = element_line(color = "grey91", size = .5),
  # The length of the axis ticks is increased.
  axis.ticks.length.x = unit(1.3, "lines"),
  axis.ticks.length.y = unit(.7, "lines"),
  # Remove the grid lines that come with ggplot2 plots by default
  panel.grid = element_blank(),
  # Customize margin values (top, right, bottom, left)
  plot.margin = margin(20, 40, 20, 40),
  # Use a light grey color for the background of both the plot and the panel
  plot.background = element_rect(fill = "grey98", color = "grey98"),
  panel.background = element_rect(fill = "grey98", color = "grey98"),
  # Customize title appearence
  plot.title = element_text(
    color = "grey10", 
    size = 28, 
    face = "bold",
    margin = margin(t = 15)
  ),
  # Customize subtitle appearence
  plot.subtitle = element_markdown(
    color = "grey30", 
    size = 16,
    lineheight = 1.35,
    margin = margin(t = 15, b = 40)
  ),
  # Title and caption are going to be aligned
  plot.title.position = "plot",
  plot.caption.position = "plot",
  plot.caption = element_text(
    color = "grey30", 
    size = 13,
    lineheight = 1.2, 
    hjust = 0,
    margin = margin(t = 40) # Large margin on the top of the caption.
  ),
  # Remove legend
  legend.position = "none"
)

plt <- ggplot(
  # The ggplot object has associated the data for the highlighted countries
  DATA, 
  aes(nameProblem,algorithm,nodesGenerated)
) + 
  # Geometric annotations that play the role of grid lines
  geom_vline(
    #xintercept = seq(2000, 2020, by = 5),
    color = "grey91", 
    size = .6
  ) +
  geom_segment(
    #data = tibble(y = seq(-4, 3, by = 1), x1 = 2000, x2 = 2020),
    #aes(x = x1, xend = x2, y = y, yend = y),
    inherit.aes = FALSE,
    color = "grey91",
    size = .6
  ) +
  geom_segment(
    #data = tibble(y = 0, x1 = 2000, x2 = 2020),
    #aes(x = x1, xend = x2, y = y, yend = y),
    inherit.aes = FALSE,
    color = "grey60",
    size = .8
  ) +
  geom_vline(
    #aes(xintercept = ref_year), 
    color = "grey40",
    linetype = "dotted",
    size = .8
  ) +
  ## Lines for the non-highlighted countries
  geom_line(
    #data = df_mac_indexed_2008 %>% filter(group == "other"),
    color = "grey75",
    size = .6,
    alpha = .5
  ) +
  ## Lines for the highlighted countries.
  # It's important to put them after the grey lines
  # so the colored ones are on top
  geom_line(
    aes(color = group),
    size = .9
  )
plt
install.packages("dplyr")
library(dplyr)
# Instalar y cargar el paquete dplyr
install.packages("dplyr")
library(dplyr)

# Suponiendo que DATA es tu data frame
DATA <- data.frame(
  nameProblem = c("Problem1", "Problem2", "Problem3"),
  algorithm = c("Alg1", "Alg2", "Alg3"),
  nodesGenerated = c(100, 150, 200)
)

# Usar el operador %>%
DATA %>%
  select(nameProblem, algorithm, nodesGenerated) %>%
  group_by(nameProblem, algorithm) %>%
  summarise(totalNodes = sum(nodesGenerated))


#######################
library(ggplot2)
library(dplyr)

# Conectar a la base de datos SQLite
conn <- dbConnect(SQLite(), dbname = "C:\\googleMapsVS\\Google-Maps\\resultados_programa.db")

# Leer la tabla 'resultados' en un data frame
df <- dbReadTable(conn, "resultados")

# Cerrar la conexión a la base de datos
dbDisconnect(conn)

# Crear la gráfica
ggplot(df, aes(x = nameProblem, y = nodesGenerated, color = algorithm)) +
  geom_point() +
  labs(title = "Nodos Generados por Estrategia para Cada Problema",
       x = "Problema",
       y = "Nodos Generados",
       color = "Algoritmo") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  theme_minimal()
####################################
library(ggplot2)
library(dplyr)

# Conectar a la base de datos SQLite
conn <- dbConnect(SQLite(), dbname = "C:\\googleMapsVS\\Google-Maps\\resultados_programa.db")

# Leer la tabla 'resultados' en un data frame
df <- dbReadTable(conn, "resultados")

# Cerrar la conexión a la base de datos
dbDisconnect(conn)

# Crear la gráfica
ggplot(df, aes(x = nameProblem, y = nodesGenerated, color = algorithm, group = algorithm)) +
  geom_point() +
  geom_line() +
  labs(title = "Nodos Generados por Estrategia para Cada Problema",
       x = "Problema",
       y = "Nodos Generados",
       color = "Algoritmo") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  theme_minimal()
##########################################################
library(ggplot2)
library(dplyr)

# Conectar a la base de datos SQLite
conn <- dbConnect(SQLite(), dbname = "C:\\googleMapsVS\\Google-Maps\\resultados_programa.db")

# Leer la tabla 'resultados' en un data frame
df <- dbReadTable(conn, "resultados")

# Cerrar la conexión a la base de datos
dbDisconnect(conn)

# Crear la gráfica
ggplot(df, aes(x = nameProblem, y = nodesGenerated, color = algorithm, group = algorithm)) +
  geom_point() +
  geom_line() +
  labs(title = "Nodos Generados por Estrategia para Cada Problema",
       x = "Problema",
       y = "Nodos Generados",
       color = "Algoritmo") +
  theme(axis.text.x = NA,  # Ocultar los valores del eje x
        axis.ticks.x = NA) +
  scale_color_brewer(palette = "Dark2") +  # Usar una paleta de colores más oscuros
  theme_minimal()
###############################################################################
library(ggplot2)
library(dplyr)

# Conectar a la base de datos SQLite
conn <- dbConnect(SQLite(), dbname = "C:\\googleMapsVS\\Google-Maps\\resultados_programa.db")

# Leer la tabla 'resultados' en un data frame
df <- dbReadTable(conn, "resultados")

# Cerrar la conexión a la base de datos
dbDisconnect(conn)

# Crear la gráfica
ggplot(df, aes(x = as.factor(nameProblem), y = nodesGenerated, color = algorithm, group = algorithm)) +
  geom_point() +
  geom_line() +
  labs(title = "Number of Generated Nodes for each problem applying different strategies",
       x = "Problems",
       y = "Nodes Generated",
       color = "Algorithm") +
  theme(axis.text.x = element_blank(),  # Ocultar los valores del eje x
        axis.ticks.x = element_blank()) +
  scale_color_brewer(palette = "Dark2") +  # Usar una paleta de colores más oscuros
  scale_x_discrete(label = NULL)+
  theme_minimal()
#######################################################################################
library(ggplot2)
library(dplyr)

# Conectar a la base de datos SQLite
conn <- dbConnect(SQLite(), dbname = "C:\\googleMapsVS\\Google-Maps\\resultados_programa.db")

# Leer la tabla 'resultados' en un data frame
df <- dbReadTable(conn, "resultados")

# Cerrar la conexión a la base de datos
dbDisconnect(conn)

# Crear la gráfica
ggplot(df, aes(x = as.factor(nameProblem), y = nodesGenerated, color = algorithm, group = algorithm)) +
  geom_point() +
  geom_line() +
  labs(title = "Nodos Generados por Estrategia para Cada Problema",
       x = "Problema",
       y = "Nodos Generados",
       color = "Algoritmo") +
  theme(axis.text.x = element_blank(),  # Ocultar los valores del eje x
        axis.ticks.x = element_blank()) +
  scale_color_brewer(palette = "Dark2") +  # Usar una paleta de colores más oscuros
  ylim(100, NA) +  # Ajustar el límite inferior del eje y
  theme_minimal()
#########################################################################################3
library(ggplot2)
library(dplyr)

# Conectar a la base de datos SQLite
conn <- dbConnect(SQLite(), dbname = "C:\\googleMapsVS\\Google-Maps\\resultados_programa.db")

# Leer la tabla 'resultados' en un data frame
df <- dbReadTable(conn, "resultados")

# Cerrar la conexión a la base de datos
dbDisconnect(conn)

# Crear la gráfica
ggplot(df, aes(x = as.factor(nameProblem), y = nodesGenerated, color = algorithm, group = algorithm)) +
  geom_point() +
  geom_line() +
  labs(title = "Nodos Generados por Estrategia para Cada Problema",
       x = "Problema",
       y = "Nodos Generados",
       color = "Algoritmo") +
  theme(axis.text.x = element_blank(),  # Ocultar los valores del eje x
        axis.ticks.x = element_blank()) +
  scale_color_brewer(palette = "Dark2") +  # Usar una paleta de colores más oscuros
  scale_y_continuous(breaks = seq(3000, max(df$nodesGenerated), by = 1000)) +  # Mostrar solo etiquetas del eje y a partir de 3000
  scale_x_discrete()+
  theme_minimal()
##########################################################################################
library(ggplot2)
library(dplyr)
names(DATA$nameProblem) <- NA
# Conectar a la base de datos SQLite
conn <- dbConnect(SQLite(), dbname = "C:\\googleMapsVS\\Google-Maps\\resultados_programa.db")

# Leer la tabla 'resultados' en un data frame
df <- dbReadTable(conn, "resultados")

# Cerrar la conexión a la base de datos
dbDisconnect(conn)

# Crear la gráfica
ggplot(df, aes(x = as.factor(nameProblem), y = nodesGenerated, color = algorithm, group = algorithm)) +
  geom_point() +
  geom_line() +
  labs(title = "Nodos Generados por Estrategia para Cada Problema",
       x = "Problema",
       y = "Nodos Generados",
       color = "Algoritmo") +
  theme(axis.text.x = element_blank(),  # Ocultar los valores del eje x
        axis.ticks.x = element_blank(),  # Ocultar las marcas del eje x
        axis.line.x = element_blank()) +  # Ocultar la línea del eje x
  scale_color_brewer(palette = "Dark2") +  # Usar una paleta de colores más oscuros
  scale_y_continuous(breaks = seq(3000, max(df$nodesGenerated), by = 1000)) +  # Mostrar solo etiquetas del eje y a partir de 3000
  labs(NULL)+
  theme_minimal()
######################################################################################3
# Crear la gráfica
ggplot(df, aes(x = as.factor(nameProblem), y = nodesExpanded, color = algorithm, group = algorithm)) +
  geom_point() +
  geom_line() +
  labs(title = "Number of Generated Nodes for each problem applying different strategies",
       x = "Problems",
       y = "Nodes Generated",
       color = "Algorithm") +
  theme(axis.text.x = element_blank(),  # Ocultar los valores del eje x
        axis.ticks.x = element_blank()) +
  scale_color_brewer(palette = "Dark2") +  # Usar una paleta de colores más oscuros
  scale_x_discrete(label = NULL)+
  theme_minimal()
#### EXPERIMENTO ###################  
# Suponiendo que df tiene una columna 'typeProblem' que categoriza los problemas
ggplot(df, aes(x = as.factor(nameProblem), y = nodesExpanded, color = algorithm, group = algorithm)) +
  geom_point() +
  geom_line() +
  labs(title = "Number of Generated Nodes for each problem applying different strategies",
       x = "Problems",
       y = "Nodes Generated",
       color = "Algorithm") +
  theme(axis.text.x = element_blank(),  # Ocultar los valores del eje x
        axis.ticks.x = element_blank()) +
  scale_color_brewer(palette = "Dark2") +  # Usar una paleta de colores más oscuros
  scale_x_discrete(label = NULL)+
  theme_minimal() +
  facet_wrap(~ typeOfProblem, scales = "free_x", nrow = 1)  # Agrupar por tipo de problema


# I forgot to compare variables

.desc.numeric(DATA$nodesGenerated, DATA$algorithm)
