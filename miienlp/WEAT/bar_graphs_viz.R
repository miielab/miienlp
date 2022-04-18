### ============================================================================
# Author: Celia Anderson 
# Description: WEAT Bar Graphs
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

# load in custom miie graph themes
source("visualizations/supplemental/code/miie_graph_themes.R")

## Load lists of award groups (a.k.a. corpora)
source("visualizations/supplemental/code/miie_collections_list.R")

### ============================================================================
### Import Data
### ============================================================================

children_file = "text_analysis/results/weat/jan2022_children_weat_data_full.csv"
histwords_file = "text_analysis/results/weat/jan2022_histwords_weat_data.csv"

children_data = read.csv(children_file)
hist_data = read.csv(histwords_file)
children_save_location = "text_analysis/results/weat/"#"visualizations/embeddings_paper/graphs/"
histwords_save_location = "visualizations/text_analysis/graphs/word_embeddings/word2vec/histwords/"

### ============================================================================
### Setting Up Data
### ============================================================================

# Dimensions of the graphs
w = 6
h = 7.6
d = 300

groups.colors = c("Mainstream" = "#CC79A7",
                  "Diversity" = "#0072B2",
                  "People of Color" = "#D55E00",
                  "African American" = "#009E73",
                  "Ability" = "#888888",
                  "Female" = "#56B4E9",
                  "LGBTQ" = "#F0E142",
                  "Histwords" = "#E69F00")

# Set up the children data 
children_data$groups <- children_data$groups %>% as.factor()

children_data <- subset(children_data, groups != 'all')

levels(children_data$groups) <- Collection.Names
children_data$embedding <- children_data$embedding %>% as.factor()
levels(children_data$embedding)
children_data$category <- children_data$category %>% as.factor()
levels(children_data$category)
children_data$domain <- children_data$domain %>% as.factor()
levels(children_data$domain)
children_data$m_assoc <- as.numeric(children_data$m_assoc)
children_data$f_assoc <- as.numeric(children_data$f_assoc)
children_data$bias <- as.numeric(children_data$bias)
children_data$abs_bias <- as.numeric(children_data$abs_bias)
children_data$ewp <- as.numeric(children_data$ewp)

# Set up hist data
hist_data$embedding <- hist_data$embedding %>% as.factor()
levels(hist_data$embedding)
hist_data$domain <- hist_data$domain %>% as.factor()
levels(hist_data$domain)
hist_data$m_assoc <- as.numeric(hist_data$m_assoc)
hist_data$f_assoc <- as.numeric(hist_data$f_assoc)
hist_data$bias <- as.numeric(hist_data$bias)
hist_data$abs_bias <- as.numeric(hist_data$abs_bias)
hist_data$ewp <- as.numeric(hist_data$ewp)
hist_data <- subset(hist_data, decade >= 1920)

mean_hist <- group_by(hist_data, category, domain, embedding) %>%
  summarise(m_assoc = mean(m_assoc, na.rm = TRUE), f_assoc = mean(f_assoc, na.rm = TRUE), bias = mean(bias, na.rm = TRUE), abs_bias = mean(abs_bias, na.rm = TRUE), ewp = mean(ewp, na.rm = TRUE))

mean_hist$groups <- "Histwords" 
both_data <- bind_rows(mean_hist, children_data)
both_data$groups <- both_data$groups %>% as.factor()

# Add Histwords to list of Groups names 
Group_Hist.Names <- c(Collection.Names, "Histwords"="Histwords")
# Relevel Group Factor
levels(both_data$groups) <- Group_Hist.Names

arrow_label <- miie$arrow_label
arrow_label <- expression(bold("("%<-% "Male-Centered )      Gender-Centeredness      ( Female-Centered" %->%")"))

### ============================================================================
### Graphing Functions
### ============================================================================

# Plot bar graph; all values are for a single dommain
plot_one_domain <- function(d, dom, emb, title, y_value)
{
  ggplot(data=subset(d, (domain == dom & embedding == emb)), 
         aes_string(x= "groups", y = y_value, fill = "groups")) + 
    geom_bar(stat="identity") + 
    miie$theme + 
    theme_update(legend.position="none") +
    theme_update(axis.title.x =element_text(size= 16)) + 
    theme_update(axis.title.y = element_text(size = 15.5)) +
    theme_update(axis.text =element_text(size=16)) + 
    #ggtitle(title) + 
    geom_hline(aes(yintercept=0), color="black") + 
    #guides(x = guide_axis(n.dodge = 2)) + 
    xlab("\nCollection") +
    scale_fill_manual(values = groups.colors) +
    theme_update(plot.margin = unit(c(59,2,3,2), "points"))
}

# Plot male association for one domain (averaged across all decades), with one bar for each group
plot_m_assoc_one_domain <- function(d, dom, emb, title)
{
  plot_one_domain(d, dom, emb, title, 'm_assoc') + 
    ylab("Avg Pairwise Cosine Similarity") +
    ylim(0, 0.149)
}

plot_f_assoc_one_domain <- function(d, dom, emb, title)
{
  plot_one_domain(d, dom, emb, title, 'f_assoc') + 
    ylab("Avg Pairwise Cosine Similarity") +
    ylim(0, 0.149)
}

# Plot average bias for one domain (average across all decades), with one bar for each group, with histwords for reference
plot_bias_one_domain <- function(d, dom, emb, title)
{
  plot_one_domain(d, dom, emb, title, 'bias') + 
    ylab(arrow_label) +
    ylim(-0.06, 0.06)
}


### ============================================================================
### Graphs
### ============================================================================

# Jones style domains
science_figure_w2v <- plot_bias_one_domain(children_data, 'miie_science', 'w2v', 'Gender Centeredness \n in Science Domain (w2v)')
family_figure_w2v <- plot_bias_one_domain(children_data, 'miie_family', 'w2v', 'Gender Centeredness \n in Family Domain (w2v)')
arts_figure_w2v <- plot_bias_one_domain(children_data, 'miie_arts', 'w2v', 'Gender Centeredness in \n Arts Domain  (w2v)')
career_figure_w2v <- plot_bias_one_domain(children_data, 'miie_career', 'w2v', 'Gender Centeredness in \n Career Domain(w2v)')
all_figure_w2v <- plot_bias_one_domain(children_data, 'miie_all', 'w2v', 'Gender Centeredness in \n All Domains (w2v)')

hist_science_figure_w2v <- plot_bias_one_domain(both_data, 'miie_science', 'w2v', 'Gender Centeredness in \n Science Domain (w2v)')
hist_family_figure_w2v <- plot_bias_one_domain(both_data, 'family', 'w2v', 'Gender Centeredness in \n Family Domain (w2v)')
hist_arts_figure_w2v <- plot_bias_one_domain(both_data, 'miie_arts', 'w2v', 'Gender Centeredness in \n Arts Domain (w2v)')
hist_career_figure_w2v <- plot_bias_one_domain(both_data, 'miie_career', 'w2v', 'Gender Centeredness in \n Professions Domain (w2v)')
hist_all_figure_w2v <- plot_bias_one_domain(both_data, 'miie_all', 'w2v', 'Gender Centeredness in \n All Domains (w2v)')


#Comparison
# office, tools, weapons, shapes, plants, bodies_water, school, positive, negative, emotions, positive_emotions, negative_emotions
hist_business_figure_w2v <- plot_bias_one_domain(both_data, 'business', 'w2v', 'Gender Centeredness in \n Business Domain (w2v)')
hist_tools_figure_w2v <- plot_bias_one_domain(both_data, 'tools', 'w2v', 'Gender Centeredness in \n Tools Domain (w2v)')
hist_weapons_figure_w2v <- plot_bias_one_domain(both_data, 'weapons', 'w2v', 'Gender Centeredness in \n Weapons Domain (w2v)')
hist_shapes_figure_w2v <- plot_bias_one_domain(both_data, 'shapes', 'w2v', 'Gender Centeredness in \n Shapes Domain (w2v)')
hist_plants_figure_w2v <- plot_bias_one_domain(both_data, 'plants', 'w2v', 'Gender Centeredness in \n Plants Domain (w2v)')
hist_bodies_water_figure_w2v <- plot_bias_one_domain(both_data, 'bodies_water', 'w2v', 'Gender Centeredness in \n Bodies of Water Domain (w2v)')
hist_school_figure_w2v <- plot_bias_one_domain(both_data, 'school', 'w2v', 'Gender Centeredness in \n School Domain (w2v)')
hist_positive_figure_w2v <- plot_bias_one_domain(both_data, 'positive', 'w2v', 'Gender Centeredness in \n Positive Domain (w2v)')
hist_negative_figure_w2v <- plot_bias_one_domain(both_data, 'negative', 'w2v', 'Gender Centeredness in \n Negative Domain (w2v)')
hist_emotions_figure_w2v <- plot_bias_one_domain(both_data, 'emotions', 'w2v', 'Gender Centeredness in \n Emotions Domain (w2v)')
hist_positive_emotions_figure_w2v <- plot_bias_one_domain(both_data, 'positive_emotions', 'w2v', 'Gender Centeredness in \n positive_emotions Domain (w2v)')
hist_negative_emotions_figure_w2v <- plot_bias_one_domain(both_data, 'negative_emotions', 'w2v', 'Gender Centeredness in \n negative_emotions Domain (w2v)')

# Pleasantness
pleasant_figure_w2v <- plot_bias_one_domain(children_data, 'pleasant', 'w2v', 'Gender Centeredness in \n Pleasant Domain (w2v)')
unpleasant_figure_w2v <- plot_bias_one_domain(children_data, 'unpleasant', 'w2v', 'Gender Centeredness in \n Unpleasant Domain (w2v)')

hist_pleasant_figure_w2v <- plot_bias_one_domain(both_data, 'pleasant', 'w2v', 'Gender Centeredness in \n Pleasant Domain (w2v)')
hist_unpleasant_figure_w2v <- plot_bias_one_domain(both_data, 'unpleasant', 'w2v', 'Gender Centeredness in \n Unpleasant Domain (w2v)')

# Sports
sports_w2v <- plot_bias_one_domain(children_data, 'sports', 'w2v', 'Gender Centeredness in \n Sports Domain (w2v)')
hist_sports_w2v <- plot_bias_one_domain(both_data, 'sports', 'w2v', 'Gender Centeredness in \n Sports Domain (w2v)')

# Appearance
appearance_w2v <- plot_bias_one_domain(children_data, 'appearance', 'w2v', 'Gender Centeredness in \n Appearance Domain (w2v)')
hist_appearance_w2v <- plot_bias_one_domain(both_data, 'appearance', 'w2v', 'Gender Centeredness in \n Appearance Domain (w2v)')

# Body
body_w2v <- plot_bias_one_domain(children_data, 'body', 'w2v', 'Gender Centeredness in \n Body Domain (w2v)')
hist_body_w2v <- plot_bias_one_domain(both_data, 'body', 'w2v', 'Gender Centeredness in \n Body Domain (w2v)')

# Apparel
apparel_w2v <- plot_bias_one_domain(children_data, 'apparel', 'w2v', 'Gender Centeredness in \n Apparel Domain (w2v)')
hist_apparel_w2v <- plot_bias_one_domain(both_data, 'apparel', 'w2v', 'Gender Centeredness in \n Apparel Domain (w2v)')

# Animals
animals_w2v <- plot_bias_one_domain(children_data, 'animals', 'w2v', 'Gender Centeredness in \n Animals Domain (w2v)')
hist_animals_w2v <- plot_bias_one_domain(both_data, 'animals', 'w2v', 'Gender Centeredness in \n Animals Domain (w2v)')

# Age-Gender
age_gender_1_w2v = plot_f_assoc_one_domain(children_data, 'female_to_male', 'w2v', 'Association Between \n Male and Female Words  (w2v)')
age_gender_2_w2v = plot_f_assoc_one_domain(children_data, 'young_female_to_old_female', 'w2v','Association Between \n Young Female and Old Female Words  (w2v)')
age_gender_3_w2v = plot_f_assoc_one_domain(children_data, 'young_female_to_old_male', 'w2v','Association Between \n Young Female and Old Male Words  (w2v)')
age_gender_4_w2v = plot_f_assoc_one_domain(children_data, 'young_to_old', 'w2v','Association Between \n Young and Old Words  (w2v)')
age_gender_5_w2v = plot_f_assoc_one_domain(children_data, 'old_female_to_old_male','w2v', 'Association Between \n Old Female and Old Male Words  (w2v)')
age_gender_6_w2v = plot_f_assoc_one_domain(children_data, 'young_female_to_old_male', 'w2v', 'Association Between \n Young Female and Old Male Words  (w2v)')
age_gender_7_w2v = plot_f_assoc_one_domain(children_data, 'young_female_to_young_male', 'w2v','Association Between \n Young Female and Young Male Words  (w2v)')
age_gender_8_w2v = plot_f_assoc_one_domain(children_data, 'young_male_to_old_female', 'w2v', 'Association Between \n Young Male and Old Female Words  (w2v)')
age_gender_9_w2v = plot_f_assoc_one_domain(children_data, 'young_male_to_old_male', 'w2v', 'Association Between \n Young Male and Old Male Words  (w2v)')

hist_age_gender_1_w2v = plot_f_assoc_one_domain(both_data, 'female_to_male', 'w2v', 'Association Between \n Male and Female Words  (w2v)')
hist_age_gender_2_w2v = plot_f_assoc_one_domain(both_data, 'young_female_to_old_female', 'w2v','Association Between \n Young Female and Old Female Words  (w2v)')
hist_age_gender_3_w2v = plot_f_assoc_one_domain(both_data, 'young_female_to_old_male', 'w2v','Association Between \n Young Female and Old Male Words  (w2v)')
hist_age_gender_4_w2v = plot_f_assoc_one_domain(both_data, 'young_to_old', 'w2v','Association Between \n Young and Old Words  (w2v)')
hist_age_gender_5_w2v = plot_f_assoc_one_domain(both_data, 'old_female_to_old_male','w2v', 'Association Between \n Old Female and Old Male Words  (w2v)')
hist_age_gender_6_w2v = plot_f_assoc_one_domain(both_data, 'young_female_to_old_male', 'w2v', 'Association Between \n Young Female and Old Male Words  (w2v)')
hist_age_gender_7_w2v = plot_f_assoc_one_domain(both_data, 'young_female_to_young_male', 'w2v','Association Between \n Young Female and Young Male Words  (w2v)')
hist_age_gender_8_w2v = plot_f_assoc_one_domain(both_data, 'young_male_to_old_female', 'w2v', 'Association Between \n Young Male and Old Female Words  (w2v)')
hist_age_gender_9_w2v = plot_f_assoc_one_domain(both_data, 'young_male_to_old_male', 'w2v', 'Association Between \n Young Male and Old Male Words  (w2v)')


### ============================================================================
### Saving Graphs
### ============================================================================

ggsave(paste(children_save_location, "family_w2v.png", sep = ""), hist_family_figure_w2v, width = w, height = h, dpi = d)
ggsave(paste(children_save_location, "business_w2v.png", sep = ""), hist_business_figure_w2v, width = w, height = h, dpi = d)
ggsave(paste(children_save_location, "appearance_w2v.png", sep = ""), hist_appearance_w2v, width = w, height = h, dpi = d)

#ggsave(paste(children_save_location, "apparel_w2v.png", sep = ""), hist_apparel_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "professions_w2v.png", sep = ""), hist_career_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "tools_w2v.png", sep = ""), hist_tools_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "weapons_w2v.png", sep = ""), hist_weapons_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "shapes_w2v.png", sep = ""), hist_shapes_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "plants_w2v.png", sep = ""), hist_plants_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bodies_water_w2v.png", sep = ""), hist_bodies_water_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "school_w2v.png", sep = ""), hist_school_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "positive_w2v.png", sep = ""), hist_positive_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "negative_w2v.png", sep = ""), hist_negative_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "emotions_w2v.png", sep = ""), hist_emotions_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "positive_emotions_w2v.png", sep = ""), hist_positive_emotions_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "negative_emotions_w2v.png", sep = ""), hist_negative_emotions_figure_w2v, width = w, height = h, dpi = d)

# 
# ggsave(paste(children_save_location, "bar_miie_science_w2v.png", sep = ""), science_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_miie_family_w2v.png", sep = ""), family_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_miie_arts_w2v.png", sep = ""), arts_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_miie_career_w2v.png", sep = ""), career_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_miie_all_w2v.png", sep = ""), all_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_pleasant_w2v.png", sep = ""), pleasant_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_unpleasant_w2v.png", sep = ""), unpleasant_figure_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_sports_w2v.png", sep = ""), sports_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender1_w2v.png", sep = ""), age_gender_1_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender2_w2v.png", sep = ""), age_gender_2_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender3_w2v.png", sep = ""), age_gender_3_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender4_w2v.png", sep = ""), age_gender_4_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender5_w2v.png", sep = ""), age_gender_5_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender6_w2v.png", sep = ""), age_gender_6_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender7_w2v.png", sep = ""), age_gender_7_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender8_w2v.png", sep = ""), age_gender_8_w2v, width = w, height = h, dpi = d)
# ggsave(paste(children_save_location, "bar_age-gender9_w2v.png", sep = ""), age_gender_9_w2v, width = w, height = h, dpi = d)

#ggsave(paste(children_save_location, "science_w2v.png", sep = ""), hist_science_figure_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "arts_w2v.png", sep = ""), hist_arts_figure_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "pleasant_w2v.png", sep = ""), hist_pleasant_figure_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "unpleasant_w2v.png", sep = ""), hist_unpleasant_figure_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "sports_w2v.png", sep = ""), hist_sports_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "age-gender/age_gender_1_w2v.png", sep = ""), hist_age_gender_1_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "age-gender/age_gender_2_w2v.png", sep = ""), hist_age_gender_2_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "age-gender/age_gender_3_w2v.png", sep = ""), hist_age_gender_3_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "age-gender/age_gender_4_w2v.png", sep = ""), hist_age_gender_4_w2v, width = w, height = h, dpi = d)#
#ggsave(paste(children_save_location, "age-gender/age_gender_5_w2v.png", sep = ""), hist_age_gender_5_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "age-gender/age_gender_6_w2v.png", sep = ""), hist_age_gender_6_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "age-gender/age_gender_7_w2v.png", sep = ""), hist_age_gender_7_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "age-gender/age_gender_8_w2v.png", sep = ""), hist_age_gender_8_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "age-gender/age_gender_9_w2v.png", sep = ""), hist_age_gender_9_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "body_w2v.png", sep = ""), hist_body_w2v, width = w, height = h, dpi = d)
#ggsave(paste(children_save_location, "animals_w2v.png", sep = ""), hist_animals_w2v, width = w, height = h, dpi = d)


