library(dplyr)
library(shiny)
library(networkD3)
library(igraph)
library(ggplot2)

db = as.data.frame(read.csv("./util_df.csv"))

EmotionalDB = as.data.frame(read.csv("./MainDB.csv"))
my_list = as.list(names(EmotionalDB))
my_list = my_list[c(2, 3, 4, 5, 6, 7, 8, 9, 10, 11)]

number_of_tweets = data.frame(DATE=c('2018-05-01' , '2018-06-01', 
                                     '2018-07-01', '2018-08-01', 
                                     '2018-09-01', '2018-10-01', 
                                     '2018-11-01', '2018-12-01', 
                                     '2019-01-01','2019-02-01',
                                     '2019-03-01','2019-04-01',
                                     '2019-05-19', '2019-05-20',
                                     '2019-05-21', '2019-05-22', 
                                     '2019-05-23', '2019-05-24',
                                     '2019-05-25', '2019-05-26'))

number_of_tweets[, "TWEETS"] = c(1856, 2832, 2898, 4873, 11341, 13101, 
                                 13963, 14369, 24153, 27429, 54790, 
                                 54790, 204295, 15886, 18471, 20691,
                                 30966, 75639, 26102, 13689)
# Convert character to Date
number_of_tweets$DATE =  as.Date(number_of_tweets$DATE, format = "%Y-%m-%d")

search_words = data.frame(SEARCHWORD = c("#EE2019", "#ThisTimeImVoting", "#EuropeanElections2019",
                                         "european elections", "ep2019", "#EUElections2019",
                                         "EU vote", "#EU vote", "#EU elections", "EU elections",
                                         "#EU #vote", "europe vote", "european vote"))

search_words[, "NUMBER"] = c(10030, 41492, 41648, 207810,
                             95449, 168699, 153896, 14819, 16769,
                             234478, 9104, 103020, 24539)

ui <- fluidPage(
  
  titlePanel("Tweets about European Elections 2019"),
  
  sidebarPanel("Total number of tweets: 999448"),
  sidebarPanel("# of tweets in 2019: 667064"),
  sidebarPanel("# of tweets in May 2019: 405739"),
  
  ########
  mainPanel(
    h3("Emotion distribution"),
    br()
  ),
  
  column(12, wellPanel(
    dateRangeInput('dateRangeEmotions',
                   label = 'Filter emotions by date',
                   start = as.Date('2019-05-20') , 
                   end = as.Date('2019-05-26')
    )
  )),
  
  selectInput("data1",
              label = "Choose an Emotion",
              choices = my_list
              
  ),
  
  plotOutput("Emotions"),
  ###############
  
  mainPanel(
    h3("Tweets' DB"),
    br()
  ),
  
  dataTableOutput('db'),
  
  mainPanel(
    h3("Employed keywords"),  
    br()),
  
  dataTableOutput('words_search'),
  
  plotOutput("Keyword_Plot"),
  
  mainPanel(
    h3("Tweets per month - Tweets per day"),
    br()
    ),
  
  column(12, wellPanel(
    dateRangeInput('dateRange',
                   label = 'Filter tweets by date',
                   start = as.Date('2018-05-01') , end = as.Date('2019-05-26')
    )
  )),
  column(12,
         dataTableOutput('my_table')
  ),
  
  plotOutput("Tweets_Plot")
  
)

server <- function(input, output, session) {
 
  EmotionalDB$Date <- as.Date(EmotionalDB$Date)
  
  selectedData <- reactive({
    subset(EmotionalDB[ , c("Date", input$data1)], Date >= input$dateRangeEmotions[1] & Date <= input$dateRangeEmotions[2])
  })
  
  output$Emotions <- renderPlot({
    sd <- selectedData()
    plot(sd, main="Emotions", type="l", xaxt = "n")
    axis.Date(side = 1, at = sd$Date, format = "%Y-%m-%d")
  })
  
  output$my_table  <- renderDataTable({
    # Filter the data
    number_of_tweets %>% filter(DATE >= input$dateRange[1] & DATE <= input$dateRange[2])
  })
  
  output$Keyword_Plot <- renderPlot({
    
    x <- search_words$SEARCHWORD
    y <- search_words$NUMBER
    par(cex.axis=0.5)
    plot(main = "Employed keywords", x, y, las=2)
    
  })
  
  output$Tweets_Plot <- renderPlot({
    x <- number_of_tweets$DATE
    y <-  number_of_tweets$TWEETS
    plot(main="Number of tweets per month", x, y, type="l", xlim=c(input$dateRange[1],input$dateRange[2]), xaxt = "n")
    axis.Date(side = 1, at = x, format = "%Y-%m-%d")
  }) 
  
  output$words_search <- renderDataTable({
    search_words
  })
  
  output$db <- renderDataTable({
    db
  })
  
}

shinyApp(ui = ui, server = server)
