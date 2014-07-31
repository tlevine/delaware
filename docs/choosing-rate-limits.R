N <- 8e6
ip.addresses <- 10 * 2^(1:6)
daily.quota <- 100 * 2^(1:6)

plot(0, 0, main = 'What should the daily quota be?',
     xlab = 'Daily request quota',
     xlim = c(0, max(daily.quota)),
     ylab = 'How many days to download all the data',
     ylim = c(0, 2*N/(min(daily.quota) * min(ip.addresses))),
     type = 'n', bty = 'l'
)
