### ============================================================================
# Author: Celia Anderson
# Description: WEAT Line Graphs
# Inputs: /project2/adukia/miie/visualizations/text_analysis/clean_data
# Outputs: /project2/adukia/miie/visualizations/text_analysis/graphs/word_embeddings
### ============================================================================

### Setup ----------------------------------------------------------------------
# set working directory
setwd("/project2/adukia/miie/")
# This is the working directory when you are running R through thinlinc
# If you are running R on your own computer, this will need to be replaced to
# whatever you named the drive when you mapped it to your computer e.g.
#setwd("M:/")

options(stringsAsFactors = FALSE)

# load in packages
library("readxl")
library("magrittr")
library("dplyr")
library("ggplot2")
library("yaml") 

# load in custom miie graph themes
source("visualizations/supplemental/code/miie_graph_themes.R")

## Load lists of award groups (a.k.a. corpora)
source("visualizations/supplemental/code/miie_collections_list.R")

### ============================================================================
### Import Data
### ============================================================================

children_file = "text_analysis/results/weat/jan2022_children_weat_data.csv"
histwords_file = "text_analysis/results/weat/jan2022_histwords_weat_data.csv"

yaml_inputs = yaml.load_file("input.yaml")
children_data = read.csv(children_file)
hist_data = read.csv(histwords_file)

children_save_location = "visualizations/embeddings_paper/graphs/"
histwords_save_location = "visualizations/text_analysis/graphs/word_embeddings/word2vec/histwords/"

### ============================================================================
### Setting Up Data
### ============================================================================

# Graph parameters
linewidth = 0.9
pointsize = 2.1

# Dimensions of the graphs 
w = 8
h = 7.6

# Min/Max Decades
min_decade = 1920
max_decade = 2010


Domain.Names    <- list("Female to Male" = "female_to_male",
                        "Old Female to Old Male" = "old_female_to_old_male",
                        "Young Female to Old Male" = "young_female_to_old_male",
                        "Young Female to Old Female" = "young_female_to_old_female",
                        "Young Female to Young Male" = "young_female_to_young_male" ,
                        "Young Male to Old Male" = "young_male_to_old_male",
                        "Young Male to Old Female" = "young_male_to_old_female" ,
                        "Young to Old" = "young_to_old",
                        "Pleasant" = "pleasant",
                        "Unpleasant" = "unpleasant",
                        "Sports" = "sports",
                        "Professions" = "miie_career",
                        "Arts" = "miie_arts",
                        "Science" = "miie_science",
                        "Family"="family",
                        "Appearance" = "appearance",
                        "Apparel" = "apparel",
                        "Body" = "body",
                        "Animals" = "animals",
                        "Office" = "office",
                        "Tools" = "tools",
                        "Weapons" = "weapons",
                        "Shapes" = "shapes",
                        "Plants" = "plants",
                        "School" = "school",
                        "Bodies of Water" = "bodies_water",
                        "Positive" = "positive",
                        "Negative" = "negative",
                        "Emotions" = "emotions",
                        "Positive Emotions" = "positive_emotions",
                        "Negative Emotions" = "negative_emotions",
                        "Business" = "business")


# Set up the children data
children_data$groups <- children_data$groups %>% as.factor()
children_data <- subset(children_data)
levels(children_data$groups) <- Collection.Names
children_data$embedding <- children_data$embedding %>% as.factor()
levels(children_data$embedding)
children_data$category <- children_data$category %>% as.factor()
levels(children_data$category)
children_data$domain <- children_data$domain %>% as.factor()
levels(children_data$domain) <- Domain.Names
children_data$m_assoc <- as.numeric(children_data$m_assoc)
children_data$f_assoc <- as.numeric(children_data$f_assoc)
children_data$bias <- as.numeric(children_data$bias)
children_data$abs_bias <- as.numeric(children_data$abs_bias)
children_data$ewp <- as.numeric(children_data$ewp)

groups.colors = c("Mainstream" = "#CC79A7",
                  "Diversity" = "#0072B2",
                  "People of Color" = "#D55E00",
                  "African American" = "#009E73",
                  "Ability" = "#888888",
                  "Female" = "#56B4E9",
                  "LGBTQ" = "#F0E142",
                  "Histwords" = "#E69F00",
                  "Children" = "#661100",
                  "Female to Male" = "#CC79A7",
                  "Old Female to Old Male" = "#0072B2",
                  "Young Female to Old Male" = "#D55E00",
                  "Young Female to Old Female" = "#009E73",
                  "Young Female to Young Male" = "#888888" ,
                  "Young Male to Old Male" = "#56B4E9",
                  "Young Male to Old Female" = "#F0E142" ,
                  "Young to Old" = "#E69F00",
                  "Pleasant" = "#CC79A7",
                  "Unpleasant" = "#0072B2",
                  "Sports" = "#CC79A7",
                  "Career" = "#CC79A7",
                  "Arts" = "#0072B2",
                  "Science" = "#D55E00",
                  "Family"="#009E73")

childrenhist.colors = c("Children" = "#661100",
                        "Histwords" = "#E69F00")

# Set up hist data
Group_Hist.Names <- c(Collection.Names, "Histwords"="histwords")
hist_data$groups <- hist_data$groups %>% as.factor()
levels(hist_data$groups) <- Group_Hist.Names
hist_data$embedding <- hist_data$embedding %>% as.factor()
levels(hist_data$embedding)
hist_data$domain <- hist_data$domain %>% as.factor()
levels(hist_data$domain) <- Domain.Names
hist_data$m_assoc <- as.numeric(hist_data$m_assoc)
hist_data$f_assoc <- as.numeric(hist_data$f_assoc)
hist_data$bias <- as.numeric(hist_data$bias)
hist_data$abs_bias <- as.numeric(hist_data$abs_bias)
hist_data$ewp <- as.numeric(hist_data$ewp)


children_data = subset(children_data, decade >= min_decade & decade <= max_decade)
hist_data = subset(hist_data, decade >= min_decade & decade <= max_decade)

jones_data = subset(children_data, category == 'jones')
comparison_data = subset(children_data, category == 'comparison')
pleasant_data = subset(children_data, category == 'pleasantness')
family_data = subset(children_data, category == 'age-gender')
sports_data = subset(children_data, category == 'sports')
appearance_data = subset(children_data, category == 'appearance')
animals_data = subset(children_data, category == 'animals')


### ============================================================================
### Merge Children's Data with Hist Data
### ============================================================================

both_data <- bind_rows(hist_data, children_data)
both_data$groups <- both_data$groups %>% as.factor()

# Add Histwords to list of Groups names

# Relevel Group Factor
#levels(both_data$groups) <- Group_Hist.Names

arrow_label <- miie$arrow_label
arrow_label <- expression(bold("("%<-% "Male-Centered )      Gender-Centeredness      ( Female-Centered" %->%")"))

### ============================================================================
### Graphing Function Helpers
### ============================================================================

add_details_to_plot <- function(p, title)
{
  decade_labels <- seq(min_decade, max_decade, by = 10)
  p + 
    miie$theme +
    geom_hline(aes(yintercept = 0), color="black") +
    #miie$emb_lines +
    #ggtitle(title) +
    xlab("\nDecade") +
    theme_update(axis.title.x =element_text(size= 16)) + 
    theme_update(axis.title.y = element_text(size = 15.5)) +
    theme_update(axis.text.x =element_text(size=16)) + 
    theme_update(axis.text.y = element_text(size=16)) +
    theme_update(legend.text = element_text(size=14))+
    theme_update(legend.position="right") +
    scale_x_continuous(breaks = decade_labels, limits = c(min_decade, max_decade)) +
    theme_update(plot.margin = unit(c(59,2,3,2), "points"))
}

# Add details for any graphs that are plotting cosine similarity
add_details_cosine_similarity <- function(p)
{
  p + 
    ylab("Avg Pairwise Cosine Similarity") +
    ylim(-0.21, 0.21)
}

# Add details for any graphs that are plotting gender centeredness
add_details_centeredness <- function(p)
{
  p + 
    ylab(arrow_label) +
    ylim(-0.06, 0.06)
}

### ============================================================================
### Graphing Functions
### ============================================================================

# Plot average association for all children groups alongside
# the histwords
plot_one_domain_assoc_per_group <- function(d, emb, dom, title) {
  d <- group_by(d, groups, domain, decade, embedding) %>%
    summarise(m_assoc = mean(m_assoc, na.rm = TRUE), f_assoc = mean(f_assoc, na.rm = TRUE))
  d <- subset(d, embedding == emb & domain == dom)
  
  p <- ggplot(data = d, aes(x = decade, color = variable, shape = variable)) +
    geom_line(aes(y = f_assoc, color = groups, shape = groups, linetype = 'f_assoc'), lwd = linewidth)+
    geom_line(aes(y= m_assoc, color = groups, shape = groups, linetype = 'm_assoc'), lwd = linewidth) +
    geom_point(aes(y = f_assoc, color = groups, shape = groups), size = pointsize) +
    geom_point(aes(y = m_assoc, color = groups, shape = groups), size = pointsize)
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p) +
    scale_colour_manual(values = groups.colors)
}

# Plot average association for all children groups alongside
# the histwords
plot_one_domain_assoc_per_group_hist <- function(d1, d2, emb, dom, title) {
  d1 <- group_by(d1, groups, domain, decade, embedding) %>%
    summarise(m_assoc = mean(m_assoc, na.rm = TRUE), f_assoc = mean(f_assoc, na.rm = TRUE))
  d1 <- subset(d1, embedding == emb & domain == dom)
  d2 <- subset(d2, embedding == emb & domain == dom)
  plot_one_domain_assoc_per_group(d1, emb, dom, title) + 
    geom_line(data = d2, aes(y = f_assoc, color = "Histwords", shape = "Histwords", linetype = 'f_assoc'), lwd = linewidth) +
    geom_line(data = d2, aes(y= m_assoc, color = "Histwords", shape = "Histwords", linetype = "m_assoc"), lwd = linewidth) +
    geom_point(data = d2, aes(y = f_assoc, color = "Histwords", shape = "Histwords"), size = pointsize) +
    geom_point(data = d2, aes(y = m_assoc, color = "Histwords", shape = "Histwords"), size = pointsze)
}

# Plot average association for all children groups alongside
# the histwords
plot_one_domain_assoc_all_groups_hist <- function(d1, d2, emb, dom, title) {
  d1 <- group_by(d1, domain, decade, embedding) %>%
    summarise(m_assoc = mean(m_assoc, na.rm = TRUE), f_assoc = mean(f_assoc, na.rm = TRUE))
  d1 <- subset(d1, embedding == emb & domain == dom)
  d2 <- subset(d2, embedding == emb & domain == dom)
  p <- ggplot(data = d1, aes(x = decade, color = variable, shape = variable)) +
    geom_line(data = d1, aes(y = f_assoc, color = "Children", shape = "Female\nAssociation\n"), lwd = linewidth)+
    geom_line(data = d1, aes(y= m_assoc, color = "Children", shape = "Male\nAssociation"), lwd = linewidth) +
    geom_point(data = d1, aes(y = f_assoc, color = "Children", shape = "Female\nAssociation\n"), size = pointsize) +
    geom_point(data = d1, aes(y = m_assoc, color = "Children", shape = "Male\nAssociation"), size = pointsize) +
    geom_line(data = d2, aes(y = f_assoc, color = "Histwords", shape = "Female\nAssociation\n")) +
    geom_line(data = d2, aes(y= m_assoc, color = "Histwords", shape = "Male\nAssociation")) +
    geom_point(data = d2, aes(y = f_assoc, color = "Histwords", shape = "Female\nAssociation\n"), size = pointsize) +
    geom_point(data = d2, aes(y = m_assoc, color = "Histwords", shape = "Male\nAssociation"), size = pointsize) 
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p) +
    scale_colour_manual(values = childrenhist.colors)
}

# Average of absolute value of bias from all the domains for each group
plot_composite_bias_per_group <- function(d, emb, title) {
  d <- group_by(d, groups, decade, embedding) %>%
    summarise(composite_bias = mean(abs_bias, na.rm = TRUE))
  p <- ggplot(data = subset(d, embedding == emb), aes(x = decade, y = composite_bias, color = groups))
  add_details_to_plot(p, title) +
    geom_point(aes(shape = groups), size = pointsize) +
    geom_line(aes(linetype = groups), lwd = linewidth) +
    ylab("Composite Bias") +
    scale_colour_manual(values = groups.colors)
}


# Plot average (across all groups) male and average female assocation for one domain. No histwords
plot_one_domain_assoc_all_groups <- function(d, emb, dom, title) {
  d <- group_by(d, domain, decade, embedding) %>%
    summarise(m_assoc = mean(m_assoc, na.rm = TRUE), f_assoc = mean(f_assoc, na.rm = TRUE))
  p <- ggplot(data = subset(d, embedding == emb & domain == dom), 
              aes(x = decade, color = variable)) +
    geom_line(aes(y = f_assoc, color = "Female\nAssociation\n"), lwd = linewidth) +
    geom_line(aes(y= m_assoc, color = "Male\nAssociation"), lwd = linewidth) +
    geom_point(aes(y = f_assoc, color = "Female\nAssociation\n"), size = pointsize) +
    geom_point(aes(y = m_assoc, color = "Male\nAssociation"), size = pointsize)
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p) +
    scale_colour_manual(values = groups.colors)
}

# Graphs male bias separately for each of the groups for one of the domains. No hist
plot_one_domain_bias_per_group <- function(d, emb, dom, title) {
  p <- ggplot(data = subset(d, embedding == emb & domain == dom), 
              aes(x = decade, y = bias, color = groups)) +
    geom_point(aes(shape = groups), size = pointsize) +
    geom_line(aes(linetype = groups), lwd = linewidth) 
  
  p <- add_details_to_plot(p, title)
  add_details_centeredness(p) +
    scale_colour_manual(values = groups.colors)
}

# Graphs average male bias (across all groups) separately for each of the domains on the same plot. No hist
plot_bias_per_domain <- function(d, emb, title) {
  d <- group_by(d, domain, decade, embedding) %>%
    summarise(bias = mean(bias, na.rm = TRUE))
  p <- ggplot(data = subset(d, embedding == emb),
              aes(x = decade, y = bias, color = domain)) +
    geom_point(size = pointsize) +
    geom_line(lwd = linewidth) 
  
  p <- add_details_to_plot(p, title)
  add_details_centeredness(p) 
}

plot_bias_per_domain_with_hist <- function(d1, d2, emb, title) {
  d1 <- group_by(d1, domain, decade, embedding) %>%
    summarise(bias = mean(bias, na.rm = TRUE))
  d1 <- subset(d1, embedding == emb)
  d2 <- subset(d2, embedding == emb)
  p <- ggplot(data = d1, aes(x = decade, color = variable, shape = domain, linetype = domain)) +
    geom_line(aes(y = bias, color = "Children"), lwd = linewidth)+
    geom_point(aes(y = bias, color = "Children"), size = pointsize) +
    geom_line(data = d2, aes(y = bias, color = "Histwords"), lwd = linewidth) +
    geom_point(data = d2, aes(y = bias, color = "Histwords"), size = pointsize) 
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p) +
    scale_colour_manual(values = childrenhist.colors)
}

# Graphs association (across all groups) separately for one of the domains on the same plot. No hist
plot_assoc_all_groups <- function(d, emb, dom, title) {
  d <- group_by(d, domain, decade, embedding) %>%
    summarise(f_assoc = mean(f_assoc, na.rm = TRUE))
  p <- ggplot(data = subset(d, embedding == emb & domain == dom), 
              aes(x = decade, y = f_assoc, color = domain)) +
    ggtitle(title)  +
    geom_point(size = pointsize) +
    geom_line(lwd = linewidth) 
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p) +
    scale_colour_manual(values = groups.colors)
}

# Plot association for each of the children groups
plot_assoc_per_group <- function(d1, emb, dom, title) {
  d1 <- group_by(d1, groups, domain, decade, embedding) %>%
    summarise(f_assoc = mean(f_assoc, na.rm = TRUE))
  d1 <- subset(d1, embedding == emb & domain == dom)
  p<- ggplot(data = d1, aes(x = decade, color = variable, shape = variable)) +
    geom_line(aes(y = f_assoc, color = groups, shape = groups), lwd = linewidth)+
    geom_point(aes(y = f_assoc, color = groups, shape = groups), size = pointsize) 
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p) +
    scale_colour_manual(values = groups.colors)
}

# Plot association for each of the children groups alongside
# the histwords
plot_assoc_per_group_with_hist <- function(d1, d2, emb, dom, title) {
  d1 <- group_by(d1, groups, domain, decade, embedding) %>%
    summarise(f_assoc = mean(f_assoc, na.rm = TRUE))
  d1 <- subset(d1, embedding == emb & domain == dom)
  d2 <- subset(d2, embedding == emb & domain == dom)
  p<- ggplot(data = d1, aes(x = decade, color = variable, shape = variable)) +
    geom_line(aes(y = f_assoc, color = groups, shape = groups), lwd = linewidth)+
    geom_point(aes(y = f_assoc, color = groups, shape = groups), size = pointsize) +
    geom_line(data = d2, aes(y = f_assoc, color = "Histwords", shape = "Histwords"), lwd = linewidth) +
    geom_point(data = d2, aes(y = f_assoc, color = "Histwords", shape = "Histwords"), size = pointsize) 
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p) +
    scale_colour_manual(values = groups.colors)
}

# Plot average association for all children groups alongside
# the histwords
plot_each_assoc_in_category <- function(d1, emb, cat, title) {
  d1 <- group_by(d1, category, domain, decade, embedding) %>%
    summarise(f_assoc = mean(f_assoc, na.rm = TRUE))
  d1 <- subset(d1, embedding == emb & category == cat)
  levels(d1$domain) <- Domain.Names
  p<- ggplot(data = d1, aes(x = decade, color = domain, shape = domain)) +
    geom_line(aes(y = f_assoc), lwd = linewidth)+
    geom_point(aes(y = f_assoc), size = pointsize) +
    scale_shape_manual(values = 0:9)
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p)
}


# Plot average association for all children groups alongside
# the histwords
plot_assoc_all_groups_with_hist <- function(d1, d2, emb, dom, title) {
  d1 <- group_by(d1, domain, decade, embedding) %>%
    summarise(f_assoc = mean(f_assoc, na.rm = TRUE))
  d1 <- subset(d1, embedding == emb & domain == dom)
  d2 <- subset(d2, embedding == emb & domain == dom)
  p <- ggplot(data = d1, aes(x = decade, color = variable, shape = variable)) +
    geom_line(aes(y = f_assoc, color = "Children", shape = "Children"), lwd = linewidth)+
    geom_point(aes(y = f_assoc, color = "Children", shape = "Children"), size = pointsize) +
    geom_line(data = d2, aes(y = f_assoc, color = "Histwords", shape = "Histwords")) +
    geom_point(data = d2, aes(y = f_assoc, color = "Histwords", shape = "Histwords"), size = pointsize) +
    scale_colour_manual(values = childrenhist.colors)
  
  p <- add_details_to_plot(p, title)
  add_details_cosine_similarity(p) +
    scale_colour_manual(values = childrenhist.colors)
}

### ============================================================================
### Graphs
### ============================================================================

### No histwords
jones1_w2v <- plot_composite_bias_per_group(jones_data, 'w2v', 'Composite Gender Bias \n in All Domains by Award Group (w2v)')
jones2_w2v <- plot_bias_per_domain(jones_data, 'w2v', 'Gender Centeredness \n in All Award Groups by Domain (w2v)')
jones3_w2v <- plot_one_domain_assoc_all_groups(jones_data, 'w2v', 'Family', 'Gender Associations \n in Family Domain (w2v)')
jones4_w2v <- plot_one_domain_assoc_all_groups(jones_data, 'w2v', 'Professions', 'Gender Associations \n in Career Domain (w2v)')
jones5_w2v <- plot_one_domain_assoc_all_groups(jones_data, 'w2v', 'Science', 'Gender Associations \n in Science Domain (w2v)')
jones6_w2v <- plot_one_domain_assoc_all_groups(jones_data, 'w2v', 'Arts', 'Gender Associations \n in Arts Domain (w2v)')
jones7_w2v <- plot_one_domain_bias_per_group(jones_data, 'w2v', 'Family', 'Gender Centeredness in Family Domain \n by Award Group (w2v)')
jones8_w2v <- plot_one_domain_bias_per_group(jones_data, 'w2v', 'Professions', 'Gender Centeredness in Career Domain \n by Award Group (w2v)')
jones9_w2v <- plot_one_domain_bias_per_group(jones_data, 'w2v', 'Science', 'Gender Centeredness in Science Domain \n by Award Group (w2v)')
jones10_w2v <- plot_one_domain_bias_per_group(jones_data, 'w2v', 'Arts', 'Gender Centeredness in Arts Domain \n by Award Group (w2v)')

p1_w2v <- plot_composite_bias_per_group(pleasant_data, 'w2v', 'Composite Gender Bias in \n Both Pleasant/Unpleasant Domains by Award Group (w2v)')
p2_w2v <- plot_bias_per_domain(pleasant_data, 'w2v', 'Gender Centeredness in All Award Groups \n by Pleasant/Unpleasant Domains (w2v)')
p3_w2v <- plot_one_domain_assoc_all_groups(pleasant_data, 'w2v', 'Pleasant', 'Gender Associations \n in Pleasant Domain for Children (w2v)')
p4_w2v <- plot_one_domain_assoc_all_groups(pleasant_data, 'w2v', 'Unpleasant', 'Gender Associations \n in Unpleasant Domain for Children (w2v)')
p5_w2v <- plot_one_domain_bias_per_group(pleasant_data, 'w2v', 'Pleasant', 'Gender Centeredness in Pleasant Domain \n by Award Group (w2v)')
p6_w2v <- plot_one_domain_bias_per_group(pleasant_data, 'w2v', 'Unpleasant', 'Gender Centeredness in Unpleasant Domain \n by Award Group (w2v)')

s1_w2v <- plot_bias_per_domain(sports_data, 'w2v', 'Gender Centeredness in All Award Groups by Sports Domains (w2v)')
s2_w2v <- plot_one_domain_assoc_all_groups(sports_data, 'w2v','Sports', 'Gender Associations \n in All Award Groups by Sports Domains (w2v)')
s3_w2v <- plot_composite_bias_per_group(sports_data, 'w2v', 'Composite Gender Bias in Sports Domain by Award Group (w2v)')
s4_w2v <- plot_one_domain_bias_per_group(sports_data, 'w2v', "Sports", 'Gender Centeredness in Sports Domain by Award Group (w2v)')

fam1_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Female to Male', 'Association Between \n Male and Female Words (w2v)')
fam2_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Young Female to Old Female', 'Association Between \n Young Female and Old Female Words (w2v)')
fam3_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Young Female to Old Male', 'Association Between \n Young Female and Old Male Words (w2v)')
fam4_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Young to Old', 'Association Between \n Young and Old Words (w2v)')
fam5_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Old Female to Old Male', 'Association Between \n Old Female and Old Male Words (w2v)')
fam6_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Young Female to Old Male', 'Association Between \n Young Female and Old Male Words (w2v)')
fam7_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Young Female to Young Male', 'Association Between \n Young Female and Young Male Words (w2v)')
fam8_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Young Male to Old Female', 'Association Between \n Young Male and Old Female Words (w2v)')
fam9_w2v = plot_assoc_all_groups(family_data, 'w2v', 'Young Male to Old Male', 'Association Between \n Young Male and Old Male Words (w2v)')
fam10_w2v = plot_each_assoc_in_category(children_data, 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups ')


##### With histwords
hist_jones1_w2v <- plot_composite_bias_per_group(subset(both_data, category == 'jones'), 'w2v', 'Composite Gender Bias \n in All Jones Domains by Award Group \n with Histwords (w2v)')
hist_jones2_w2v <- plot_bias_per_domain_with_hist(jones_data, subset(hist_data, category == 'jones'), 'w2v', 'Gender Centeredness in All Jones Domains \n for Children and Histwords (w2v)')
hist_jones3_w2v <- plot_bias_per_domain(jones_data, 'w2v', 'Gender Centeredness in All Jones Domains \n for Children (w2v)')
hist_jones4_w2v <- plot_bias_per_domain(subset(hist_data, category == 'jones'), 'w2v', 'Gender Centeredness in All Jones Domains \n for Histwords (w2v)')

hist_pleasantness1_w2v <- plot_composite_bias_per_group(subset(both_data, category == 'pleasantness'), 'w2v', 'Composite Gender Bias \n in All Pleasantness Domains by Award Group \n with Histwords (w2v)')
hist_pleasantness2_w2v <- plot_bias_per_domain_with_hist(pleasant_data, subset(hist_data, category == 'pleasantness'), 'w2v', 'Gender Centeredness in All Pleasantness Domains \n for Children and Histwords (w2v)')
hist_pleasantness3_w2v <- plot_bias_per_domain(pleasant_data, 'w2v', 'Gender Centeredness in All Pleasantness Domains \n for Children (w2v)')
hist_pleasantness4_w2v <- plot_bias_per_domain(subset(hist_data, category == 'pleasantness'), 'w2v', 'Gender Centeredness in All Pleasantness Domains \n for Histwords (w2v)')

hist_appearance1_w2v <- plot_composite_bias_per_group(subset(both_data, category == 'appearance'), 'w2v', 'Composite Gender Bias \n in All Appearance Domains by Award Group \n with Histwords (w2v)')
hist_appearance2_w2v <- plot_bias_per_domain_with_hist(appearance_data, subset(hist_data, category == 'appearance'), 'w2v', 'Gender Centeredness in All Appearance Domains \n for Children and Histwords (w2v)')
hist_appearance3_w2v <- plot_bias_per_domain(appearance_data, 'w2v', 'Gender Centeredness in All Appearance Domains \n for Children (w2v)')
hist_appearance4_w2v <- plot_bias_per_domain(subset(hist_data, category == 'appearance'), 'w2v', 'Gender Centeredness in All Appearance Domains \n for Histwords (w2v)')

hist_sports1_w2v <- plot_composite_bias_per_group(subset(both_data, category == 'sports'), 'w2v', 'Composite Gender Bias \n in Sports by Award Group \n with Histwords (w2v)')

hist_animals1_w2v <- plot_composite_bias_per_group(subset(both_data, category == 'animals'), 'w2v', 'Composite Gender Bias \n in Animals by Award Group \n with Histwords (w2v)')

hist_fam1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'Family', 'Gender Centeredness \n in Family Domain \n by Award Group and Histwords (w2v)')
hist_fam2_w2v <- plot_one_domain_assoc_all_groups_hist(jones_data, hist_data, 'w2v', 'Family', 'Gender Associations \n in Family Domain with Hist (w2v)')
hist_fam3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Family', 'Gender Associations \n in Family Domain with Hist (w2v)')

hist_career1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'Professions', 'Gender Centeredness \n in Career Domain \n by Award Group and Histwords (w2v)')
hist_career2_w2v <- plot_one_domain_assoc_all_groups_hist(jones_data, hist_data, 'w2v', 'Professions', 'Gender Associations \n in Career Domain with Hist (w2v)')
hist_career3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Professions', 'Gender Associations \n in Career Domain with Hist (w2v)')

hist_science1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'Science', 'Gender Centeredness \n in Science Domain \n by Award Group and Histwords (w2v)')
hist_science2_w2v <- plot_one_domain_assoc_all_groups_hist(jones_data, hist_data, 'w2v', 'Science', 'Gender Associations \n in Science Domain with Hist (w2v)')
hist_science3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Science', 'Gender Associations \n in Science Domain with Hist (w2v)')

hist_arts1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'Arts', 'Gender Centeredness \n in Arts Domain \n by Award Group and Histwords (w2v)')
hist_arts2_w2v <- plot_one_domain_assoc_all_groups_hist(jones_data, hist_data, 'w2v', 'Arts', 'Gender Associations \n in Arts Domain with Hist(w2v)')
hist_arts3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Arts', 'Gender Associations \n in Arts Domain with Hist(w2v)')

hist_business1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'business', 'Gender Centeredness \n in business Domain \n by Award Group and Histwords (w2v)')
hist_business2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'business', 'Gender Associations \n in business Domain with Hist(w2v)')
hist_business3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'business', 'Gender Associations \n in business Domain with Hist(w2v)')

hist_tools1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'tools', 'Gender Centeredness \n in tools Domain \n by Award Group and Histwords (w2v)')
hist_tools2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'tools', 'Gender Associations \n in tools Domain with Hist(w2v)')
hist_tools3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'tools', 'Gender Associations \n in tools Domain with Hist(w2v)')

hist_weapons1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'weapons', 'Gender Centeredness \n in weapons Domain \n by Award Group and Histwords (w2v)')
hist_weapons2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'weapons', 'Gender Associations \n in weapons Domain with Hist(w2v)')
hist_weapons3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'weapons', 'Gender Associations \n in weapons Domain with Hist(w2v)')

hist_shapes1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'shapes', 'Gender Centeredness \n in shapes Domain \n by Award Group and Histwords (w2v)')
hist_shapes2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'shapes', 'Gender Associations \n in shapes Domain with Hist(w2v)')
hist_shapes3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'shapes', 'Gender Associations \n in shapes Domain with Hist(w2v)')

hist_plants1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'plants', 'Gender Centeredness \n in plants Domain \n by Award Group and Histwords (w2v)')
hist_plants2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'plants', 'Gender Associations \n in plants Domain with Hist(w2v)')
hist_plants3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'plants', 'Gender Associations \n in plants Domain with Hist(w2v)')

hist_bodies_water1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'bodies_water', 'Gender Centeredness \n in bodies_water Domain \n by Award Group and Histwords (w2v)')
hist_bodies_water2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'bodies_water', 'Gender Associations \n in bodies_water Domain with Hist(w2v)')
hist_bodies_water3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'bodies_water', 'Gender Associations \n in bodies_water Domain with Hist(w2v)')

hist_school1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'school', 'Gender Centeredness \n in school Domain \n by Award Group and Histwords (w2v)')
hist_school2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'school', 'Gender Associations \n in school Domain with Hist(w2v)')
hist_school3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'school', 'Gender Associations \n in school Domain with Hist(w2v)')

hist_positive1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'positive', 'Gender Centeredness \n in positive Domain \n by Award Group and Histwords (w2v)')
hist_positive2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'positive', 'Gender Associations \n in positive Domain with Hist(w2v)')
hist_positive3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'positive', 'Gender Associations \n in positive Domain with Hist(w2v)')

hist_negative1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'negative', 'Gender Centeredness \n in negative Domain \n by Award Group and Histwords (w2v)')
hist_negative2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'negative', 'Gender Associations \n in negative Domain with Hist(w2v)')
hist_negative3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'negative', 'Gender Associations \n in negative Domain with Hist(w2v)')

hist_emotions1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'emotions', 'Gender Centeredness \n in emotions Domain \n by Award Group and Histwords (w2v)')
hist_emotions2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'emotions', 'Gender Associations \n in emotions Domain with Hist(w2v)')
hist_emotions3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'emotions', 'Gender Associations \n in emotions Domain with Hist(w2v)')

hist_positive_emotions1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'positive_emotions', 'Gender Centeredness \n in positive_emotions Domain \n by Award Group and Histwords (w2v)')
hist_positive_emotions2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'positive_emotions', 'Gender Associations \n in positive_emotions Domain with Hist(w2v)')
hist_positive_emotions3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'positive_emotions', 'Gender Associations \n in positive_emotions Domain with Hist(w2v)')

hist_negative_emotions1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'negative_emotions', 'Gender Centeredness \n in negative_emotions Domain \n by Award Group and Histwords (w2v)')
hist_negative_emotions2_w2v <- plot_one_domain_assoc_all_groups_hist(comparison_data, hist_data, 'w2v', 'negative_emotions', 'Gender Associations \n in negative_emotions Domain with Hist(w2v)')
hist_negative_emotions3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'negative_emotions', 'Gender Associations \n in negative_emotions Domain with Hist(w2v)')

hist_p1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'Pleasant', 'Gender Centeredness in Pleasant Domain \n by Award Group and Histwords (w2v)')
hist_p2_w2v <- plot_one_domain_assoc_all_groups_hist(pleasant_data, hist_data, 'w2v', 'Pleasant', 'Gender Associations \n in Pleasant Domain for Children and Histwords (w2v)')
hist_p3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Pleasant', 'Gender Associations \n in Pleasant Domain \n by Award Group and Histwords (w2v)')

hist_up1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', 'Unpleasant', 'Gender Centeredness in Unpleasant Domain \n by Award Group and Histwords (w2v)')
hist_up2_w2v <- plot_one_domain_assoc_all_groups_hist(pleasant_data, hist_data, 'w2v', 'Unpleasant', 'Gender Associations \n in Unpleasant Domain for Children and Histwords (w2v)')
hist_up3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Unpleasant', 'Gender Associations \n in Unpleasant Domain \n by Award Group and Histwords (w2v)')

hist_s1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', "Sports", 'Gender Centeredness in Sports Domain by Award Group (w2v)')
hist_s2_w2v <- plot_one_domain_assoc_all_groups_hist(sports_data, hist_data, 'w2v', 'Sports', 'Gender Associations \n in Sports Domain for Children and Histwords (w2v)')
hist_s3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Sports', 'Gender Associations \n in Sports Domain for Children and Histwords (w2v)')

hist_appear1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', "Appearance", 'Gender Centeredness in Appearance Domain by Award Group (w2v)')
hist_appear2_w2v <- plot_one_domain_assoc_all_groups_hist(appearance_data, hist_data, 'w2v', 'Appearance', 'Gender Associations \n in Appearance Domain for Children and Histwords (w2v)')
hist_appear3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Appearance', 'Gender Associations \n in Appearance Domain for Children and Histwords (w2v)')

hist_body1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', "Body", 'Gender Centeredness in Body Domain by Award Group (w2v)')
hist_body2_w2v <- plot_one_domain_assoc_all_groups_hist(appearance_data, hist_data, 'w2v', 'Body', 'Gender Associations \n in Body Domain for Children and Histwords (w2v)')
hist_body3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Body', 'Gender Associations \n in Body Domain for Children and Histwords (w2v)')

hist_cloth1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', "Apparel", 'Gender Centeredness in apparel Domain by Award Group (w2v)')
hist_cloth2_w2v <- plot_one_domain_assoc_all_groups_hist(appearance_data, hist_data, 'w2v', 'Apparel', 'Gender Associations \n in apparel Domain for Children and Histwords (w2v)')
hist_cloth3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Apparel', 'Gender Associations \n in apparel Domain for Children and Histwords (w2v)')

hist_animals1_w2v <- plot_one_domain_bias_per_group(both_data, 'w2v', "Animals", 'Gender Centeredness in Animals Domain by Award Group (w2v)')
hist_animals2_w2v <- plot_one_domain_assoc_all_groups_hist(animals_data, hist_data, 'w2v', 'Animals', 'Gender Associations \n in Animals Domain for Children and Histwords (w2v)')
hist_animals3_w2v <- plot_one_domain_assoc_per_group(both_data, 'w2v', 'Animals', 'Gender Associations \n in Animals Domain for Children and Histwords (w2v)')

hist_ag1_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Female to Male', 'Association Between \n Male and Female Words (w2v)')
hist_ag2_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Young Female to Old Female', 'Association Between \n Young Female and Old Female Words (w2v)')
hist_ag3_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Young Female to Old Male', 'Association Between \n Young Female and Old Male Words (w2v)')
hist_ag4_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Young to Old', 'Association Between \n Young and Old Words (w2v)')
hist_ag5_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Old Female to Old Male', 'Association Between \n Old Female and Old Male Words (w2v)')
hist_ag6_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Young Female to Old Male', 'Association Between \n Young Female and Old Male Words (w2v)')
hist_ag7_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Young Female to Young Male', 'Association Between \n Young Female and Young Male Words (w2v)')
hist_ag8_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Young Male to Old Female', 'Association Between \n Young Male and Old Female Words (w2v)')
hist_ag9_w2v = plot_assoc_all_groups_with_hist(family_data, hist_data, 'w2v', 'Young Male to Old Male', 'Association Between \n Young Male and Old Male Words (w2v)')

hist_ag1_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Female to Male', 'Association Between \n Male and Female Words (w2v)')
hist_ag2_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Young Female to Old Female', 'Association Between \n Young Female and Old Female Words (w2v)')
hist_ag3_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Young Female to Old Male', 'Association Between \n Young Female and Old Male Words (w2v)')
hist_ag4_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Young to Old', 'Association Between \n Young and Old Words (w2v)')
hist_ag5_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Old Female to Old Male', 'Association Between \n Old Female and Old Male Words (w2v)')
hist_ag6_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Young Female to Old Male', 'Association Between \n Young Female and Old Male Words (w2v)')
hist_ag7_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Young Female to Young Male', 'Association Between \n Young Female and Young Male Words (w2v)')
hist_ag8_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Young Male to Old Female', 'Association Between \n Young Male and Old Female Words (w2v)')
hist_ag9_allgroups_w2v = plot_assoc_per_group(both_data, 'w2v', 'Young Male to Old Male', 'Association Between \n Young Male and Old Male Words (w2v)')

hist_ag1_single_collection_w2v = plot_each_assoc_in_category(subset(family_data, groups == "Mainstream"), 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups \n in Mainstream Collection')
hist_ag2_single_collection_w2v = plot_each_assoc_in_category(subset(family_data, groups == "Diversity"), 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups \n in Diversity Collection')
hist_ag3_single_collection_w2v = plot_each_assoc_in_category(subset(family_data, groups == "People of Color"), 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups \n in People of Color Collection')
hist_ag4_single_collection_w2v = plot_each_assoc_in_category(subset(family_data, groups == "African American"), 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups \n in African American Collection')
hist_ag5_single_collection_w2v = plot_each_assoc_in_category(subset(family_data, groups == "Ability"), 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups \n in Ability Collection')
hist_ag6_single_collection_w2v = plot_each_assoc_in_category(subset(family_data, groups == "Female"), 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups \n in Female Collection')
hist_ag7_single_collection_w2v = plot_each_assoc_in_category(subset(family_data, groups == "LGBTQ"), 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups \n in LGBTQ Collection')
hist_ag8_single_collection_w2v = plot_each_assoc_in_category(hist_data, 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups \n in Histwords Collection')

##### Just histwords
histwords_p1_w2v <- plot_one_domain_assoc_all_groups(hist_data, 'w2v', 'Pleasant', 'Gender Associations \n in Pleasant Domain for Histwords (w2v)')
histwords_p2_w2v <- plot_one_domain_assoc_all_groups(hist_data, 'w2v', 'Unpleasant', 'Gender Associations \n in Unpleasant Domain for Histwords (w2v)')
hist_fam10_w2v = plot_each_assoc_in_category(hist_data, 'w2v', 'age-gender', 'Associations between \nPairs of Age/Gender Word Groups ')

### ============================================================================
### Saving graphs
### ============================================================================
# 
# ggsave(paste(children_save_location, "jones_composite_bias_w2v.png", sep = ""), hist_jones1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_bias_per_domain_1_w2v.png", sep = ""), hist_jones2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_bias_per_domain_2_w2v.png", sep = ""), hist_jones3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_bias_per_domain_3_w2v.png", sep = ""), hist_jones4_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "appearance_composite_bias_w2v.png", sep = ""), hist_appearance1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "appearance_bias_per_domain_1_w2v.png", sep = ""), hist_appearance2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "appearance_bias_per_domain_2_w2v.png", sep = ""), hist_appearance3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "appearance_bias_per_domain_3_w2v.png", sep = ""), hist_appearance4_w2v, width = w, height = h)

ggsave(paste(children_save_location, "appearance/appearance_1_w2v.png", sep = ""), hist_appear1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "appearance/appearance_2_w2v.png", sep = ""), hist_appear2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "appearance/appearance_3_w2v.png", sep = ""), hist_appear3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "apparel/apparel_1_w2v.png", sep = ""), hist_cloth1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "apparel/apparel_2_w2v.png", sep = ""), hist_cloth2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "apparel/apparel_3_w2v.png", sep = ""), hist_cloth3_w2v, width = w, height = h)
ggsave(paste(children_save_location, "family/fam_1_w2v.png", sep = ""), hist_fam1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "family/fam_2_w2v.png", sep = ""), hist_fam2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "family/fam_3_w2v.png", sep = ""), hist_fam3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "professions/professions_1_w2v.png", sep = ""), hist_career1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "professions/professions_2_w2v.png", sep = ""), hist_career2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "professions/professions_3_w2v.png", sep = ""), hist_career3_w2v, width = w, height = h)
# office, tools, weapons, shapes, plants, bodies_water, school, positive, negative, emotions, positive_emotions, negative_emotions
ggsave(paste(children_save_location, "business/business_1_w2v.png", sep = ""), hist_business1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "business/business_2_w2v.png", sep = ""), hist_business2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "business/business_3_w2v.png", sep = ""), hist_business3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "tools/tools_1_w2v.png", sep = ""), hist_tools1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "tools/tools_2_w2v.png", sep = ""), hist_tools2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "tools/tools_3_w2v.png", sep = ""), hist_tools3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "weapons/weapons_1_w2v.png", sep = ""), hist_weapons1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "weapons/weapons_2_w2v.png", sep = ""), hist_weapons2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "weapons/weapons_3_w2v.png", sep = ""), hist_weapons3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "shapes/shapes_1_w2v.png", sep = ""), hist_shapes1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "shapes/shapes_2_w2v.png", sep = ""), hist_shapes2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "shapes/shapes_3_w2v.png", sep = ""), hist_shapes3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "plants/plants_1_w2v.png", sep = ""), hist_plants1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "plants/plants_2_w2v.png", sep = ""), hist_plants2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "plants/plants_3_w2v.png", sep = ""), hist_plants3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "bodies_water/bodies_water_1_w2v.png", sep = ""), hist_bodies_water1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "bodies_water/bodies_water_2_w2v.png", sep = ""), hist_bodies_water2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "bodies_water/bodies_water_3_w2v.png", sep = ""), hist_bodies_water3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "school/school_1_w2v.png", sep = ""), hist_school1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "school/school_2_w2v.png", sep = ""), hist_school2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "school/school_3_w2v.png", sep = ""), hist_school3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "positive/positive_1_w2v.png", sep = ""), hist_positive1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "positive/positive_2_w2v.png", sep = ""), hist_positive2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "positive/positive_3_w2v.png", sep = ""), hist_positive3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "negative/negative_1_w2v.png", sep = ""), hist_negative1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "negative/negative_2_w2v.png", sep = ""), hist_negative2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "negative/negative_3_w2v.png", sep = ""), hist_negative3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "emotions/emotions_1_w2v.png", sep = ""), hist_emotions1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "emotions/emotions_2_w2v.png", sep = ""), hist_emotions2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "emotions/emotions_3_w2v.png", sep = ""), hist_emotions3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "positive_emotions/positive_emotions_1_w2v.png", sep = ""), hist_positive_emotions1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "positive_emotions/positive_emotions_2_w2v.png", sep = ""), hist_positive_emotions2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "positive_emotions/positive_emotions_3_w2v.png", sep = ""), hist_positive_emotions3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "negative_emotions/negative_emotions_1_w2v.png", sep = ""), hist_negative_emotions1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "negative_emotions/negative_emotions_2_w2v.png", sep = ""), hist_negative_emotions2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "negative_emotions/negative_emotions_3_w2v.png", sep = ""), hist_negative_emotions3_w2v, width = w, height = h)

# ggsave(paste(children_save_location, "sports/sports_composite_bias_w2v.png", sep = ""), hist_sports1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "animals/animals_composite_bias_w2v.png", sep = ""), hist_animals1_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "pleasantness_composite_bias_w2v.png", sep = ""), hist_pleasantness1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasantness_bias_per_domain_1_w2v.png", sep = ""), hist_pleasantness2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasantness_bias_per_domain_2_w2v.png", sep = ""), hist_pleasantness3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasantness_bias_per_domain_3_w2v.png", sep = ""), hist_pleasantness4_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "body/body_1_w2v.png", sep = ""), hist_body1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "body/body_2_w2v.png", sep = ""), hist_body2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "body/body_3_w2v.png", sep = ""), hist_body3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "animals/animals_1_w2v.png", sep = ""), hist_animals1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "animals/animals_2_w2v.png", sep = ""), hist_animals2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "animals/animals_3_w2v.png", sep = ""), hist_animals3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "arts/arts_1_w2v.png", sep = ""), hist_arts1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "arts/arts_2_w2v.png", sep = ""), hist_arts2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "arts/arts_3_w2v.png", sep = ""), hist_arts3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "science/science_1_w2v.png", sep = ""), hist_science1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "science/science_2_w2v.png", sep = ""), hist_science2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "science/science_3_w2v.png", sep = ""), hist_science3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasant/pleasant_1_w2v.png", sep = ""), hist_p1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasant/pleasant_2_w2v.png", sep = ""), hist_p2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasant/pleasant_3_w2v.png", sep = ""), hist_p3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "unpleasant/unpleasant_1_w2v.png", sep = ""), hist_up1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "unpleasant/unpleasant_2_w2v.png", sep = ""), hist_up2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "unpleasant/unpleasant_3_w2v.png", sep = ""), hist_up3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "sports/sports_1_w2v.png", sep = ""), hist_s1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "sports/sports_2_w2v.png", sep = ""), hist_s2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "sports/sports_3_w2v.png", sep = ""), hist_s3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_1_w2v.png", sep = ""), hist_ag1_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_2_w2v.png", sep = ""), hist_ag2_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_3_w2v.png", sep = ""), hist_ag3_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_4_w2v.png", sep = ""), hist_ag4_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_5_w2v.png", sep = ""), hist_ag5_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_6_w2v.png", sep = ""), hist_ag6_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_7_w2v.png", sep = ""), hist_ag7_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_8_w2v.png", sep = ""), hist_ag8_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_each_collection_9_w2v.png", sep = ""), hist_ag9_allgroups_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_1_w2v.png", sep = ""), hist_ag1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_2_w2v.png", sep = ""), hist_ag2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_3_w2v.png", sep = ""), hist_ag3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_4_w2v.png", sep = ""), hist_ag4_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_5_w2v.png", sep = ""), hist_ag5_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_6_w2v.png", sep = ""), hist_ag6_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_7_w2v.png", sep = ""), hist_ag7_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_8_w2v.png", sep = ""), hist_ag8_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_9_w2v.png", sep = ""), hist_ag9_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_1_w2v.png", sep = ""), hist_ag1_single_collection_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_2_w2v.png", sep = ""), hist_ag2_single_collection_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_3_w2v.png", sep = ""), hist_ag3_single_collection_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_4_w2v.png", sep = ""), hist_ag4_single_collection_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_5_w2v.png", sep = ""), hist_ag5_single_collection_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_6_w2v.png", sep = ""), hist_ag6_single_collection_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_7_w2v.png", sep = ""), hist_ag7_single_collection_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_8_w2v.png", sep = ""), hist_ag8_single_collection_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age-gender/age_gender_single_collection_9_w2v.png", sep = ""), hist_ag9_single_collection_w2v, width = w, height = h)



# ggsave(paste(children_save_location, "jones_figure1_w2v.png", sep = ""), jones1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure2_w2v.png", sep = ""), jones2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure3_w2v.png", sep = ""), jones3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure4_w2v.png", sep = ""), jones4_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure5_w2v.png", sep = ""), jones5_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure6_w2v.png", sep = ""), jones6_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure7_w2v.png", sep = ""), jones7_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure8_w2v.png", sep = ""), jones8_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure9_w2v.png", sep = ""), jones9_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure10_w2v.png", sep = ""), jones10_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "pleasantness_figure1_w2v.png", sep = ""), p1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasantness_figure2_w2v.png", sep = ""), p2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasantness_figure3_w2v.png", sep = ""), p3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasantness_figure4_w2v.png", sep = ""), p4_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasantness_figure5_w2v.png", sep = ""), p5_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "pleasantness_figure6_w2v.png", sep = ""), p6_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "hist_pleasantness1_w2v.png", sep = ""), hist_p1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_pleasantness2_w2v.png", sep = ""), hist_p2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_pleasantness3_w2v.png", sep = ""), hist_p3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_pleasantness4_w2v.png", sep = ""), hist_p4_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "all_hist_pleasantness3_w2v.png", sep = ""), all_hist_p3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_pleasantness4_w2v.png", sep = ""), all_hist_p4_w2v, width = w, height = h)
# 
# ggsave(paste(histwords_save_location, "histwords_pleasantness_figure1_w2v.png", sep = ""), histwords_p1_w2v, width = w, height = h)
# ggsave(paste(histwords_save_location, "histwords_pleasantness_figure2_w2v.png", sep = ""), histwords_p2_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "jones_figure1_w2v_with_hist.png", sep = ""), hist_figure1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure2_w2v_with_hist.png", sep = ""), hist_figure2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure3_w2v_with_hist.png", sep = ""), hist_figure3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure4_w2v_with_hist.png", sep = ""), hist_figure4_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure5_w2v_with_hist.png", sep = ""), hist_figure5_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure6_w2v_with_hist.png", sep = ""), hist_figure6_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure7_w2v_with_hist.png", sep = ""), hist_figure7_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure8_w2v_with_hist.png", sep = ""), hist_figure8_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "jones_figure9_w2v_with_hist.png", sep = ""), hist_figure9_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "all_jones_figure6_w2v_with_hist.png", sep = ""), all_hist_figure6_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_jones_figure7_w2v_with_hist.png", sep = ""), all_hist_figure7_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_jones_figure8_w2v_with_hist.png", sep = ""), all_hist_figure8_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_jones_figure9_w2v_with_hist.png", sep = ""), all_hist_figure9_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "sports_figure1_w2v.png", sep = ""), s1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "sports_figure2_w2v.png", sep = ""), s2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "sports_figure3_w2v.png", sep = ""), s3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "sports_figure4_w2v.png", sep = ""), s4_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "hist_sports_figure1_w2v.png", sep = ""), hist_s1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_sports_figure1_w2v.png", sep = ""), all_hist_s1_w2v, width = w, height = h)
# 
# 
# ggsave(paste(children_save_location, "age_gender_figure1_w2v.png", sep = ""), fam1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure2_w2v.png", sep = ""), fam2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure3_w2v.png", sep = ""), fam3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure4_w2v.png", sep = ""), fam4_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure5_w2v.png", sep = ""), fam5_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure6_w2v.png", sep = ""), fam6_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure7_w2v.png", sep = ""), fam7_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure8_w2v.png", sep = ""), fam8_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure9_w2v.png", sep = ""), fam9_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "age_gender_figure10_w2v.png", sep = ""), fam10_w2v, width = w, height = h)
# 
# ggsave(paste(children_save_location, "hist_age_gender_figure1_w2v.png", sep = ""), hist_fam1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_age_gender_figure2_w2v.png", sep = ""), hist_fam2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_age_gender_figure3_w2v.png", sep = ""), hist_fam3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_age_gender_figure4_w2v.png", sep = ""), hist_fam4_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_age_gender_figure5_w2v.png", sep = ""), hist_fam5_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_age_gender_figure6_w2v.png", sep = ""), hist_fam6_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_age_gender_figure7_w2v.png", sep = ""), hist_fam7_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_age_gender_figure8_w2v.png", sep = ""), hist_fam8_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "hist_age_gender_figure9_w2v.png", sep = ""), hist_fam9_w2v, width = w, height = h)
# 
# 
# ggsave(paste(children_save_location, "all_hist_age_gender_figure1_w2v.png", sep = ""), all_hist_fam1_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_age_gender_figure2_w2v.png", sep = ""), all_hist_fam2_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_age_gender_figure3_w2v.png", sep = ""), all_hist_fam3_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_age_gender_figure4_w2v.png", sep = ""), all_hist_fam4_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_age_gender_figure5_w2v.png", sep = ""), all_hist_fam5_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_age_gender_figure6_w2v.png", sep = ""), all_hist_fam6_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_age_gender_figure7_w2v.png", sep = ""), all_hist_fam7_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_age_gender_figure8_w2v.png", sep = ""), all_hist_fam8_w2v, width = w, height = h)
# ggsave(paste(children_save_location, "all_hist_age_gender_figure9_w2v.png", sep = ""), all_hist_fam9_w2v, width = w, height = h)
# 
# ggsave(paste(histwords_save_location, "age_gender_figure10_w2v.png", sep = ""), hist_fam10_w2v, width = w, height = h)
