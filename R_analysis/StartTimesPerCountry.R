#we only use those values
to_use = as.logical(full$country!="")&!is.na(full$hour_start_per_run)

#we need data by country, run, and user
country_hours = data.table(country = full$country[to_use], hours = full$hour_start_per_run[to_use], users = full$endo.x[to_use])

#number of runs per country
run_count = plyr::count(country_hours, 'country')

#number of users per country
user_count = country_hours[ , .(user_count=length(unique(users))), by=.(country)]

#table of frequencies
tally = merge(x = run_count, y = user_count, by="country", all.x=TRUE)
ordered_tally = tally[order(tally$freq, decreasing = TRUE), ]
ordered_tally = data.table(ordered_tally)
ordered_tally[ , run_user_ratio:=freq/user_count]

#save data for later user
working_directory="D:/data/running"
setwd(working_directory)
write.csv(ordered_tally, "country_tally.csv")
write.csv(country_hours, "country_hours.csv")
