N <- 8e6
ip.addresses <- 10 * 2^(3:6)
daily.quota <- 100 * 2^(1:4)

plot(0, 0, main = 'What should the daily quota be?',
     xlab = 'Daily request quota',
     xlim = c(0, max(daily.quota)),
     ylab = 'How many days to download all the data',
     ylim = c(0, 2*N/(min(daily.quota) * min(ip.addresses))),
     type = 'n', bty = 'n'
)

color <- 1
for (i in ip.addresses) {
    y <- 2*N/(i*daily.quota)
    lines(y ~ daily.quota, col = color)
    color <- color + 1
}
text(min(daily.quota), 2*N/(ip.addresses * min(daily.quota)),
     label = ip.addresses, pos = 2)
text(max(daily.quota)/2, 2*N/(min(ip.addresses)*min(daily.quota)),
     'Different lines are for different\namounts of IP addresses.\n(20 addresses, 40 addresses, &c.)', pos = 1)
