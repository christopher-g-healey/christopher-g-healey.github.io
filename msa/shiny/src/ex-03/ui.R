library( shiny )
shinyUI( fluidPage(
  titlePanel( "Sepal Width Boxplot" ),
  sidebarLayout(
    sidebarPanel(
      checkboxGroupInput(
        "species",
        "Species:",
        c( "Setosa" = "setosa",
           "Versicolor" = "versicolor",
           "Virginica" = "virginica"
        ),
        inline = TRUE,
        selected = "setosa"
      ),
      radioButtons(
        "points",
        "Points:",
        c( "Outlier" = "outlier", "All" = "all" ),
        inline = TRUE
      ),
      sliderInput(
        "iqr",
        "Outlier IQR:",
        min = 0.5,
        max = 3.0,
        step = 0.25,
        value = 1.5
      )
    ),
    mainPanel(
      plotOutput( "distPlot" )
    )
  )
) )
