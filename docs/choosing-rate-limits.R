N <- 8e6
ip.addresses <- 10 * 2^(3:6)
daily.quota <- 100 * 2^(1:4)

plot(0, 0, main = 'What should the rate limit be?',
     xlab = 'Number of requests that one worker makes per day',
     xlim = c(0, max(daily.quota) + 100),
     ylab = 'How many months to download all the data',
     ylim = c(0, 400),
     type = 'n', bty = 'n', axes = F
)
axis(1)
axis(2, at = ((0:12)/12) * 365, labels = 0:12, las = 1)
abline(h = 0)

color <- 1
for (i in ip.addresses) {
    y <- 2*N/(i*daily.quota)
    lines(y ~ daily.quota, col = color)
    color <- color + 1
}
text(max(daily.quota), 2*N/(ip.addresses * max(daily.quota)),
     label = ip.addresses, pos = 4)
text(max(daily.quota), 350, pos = 2,
     'Different lines are for different\namounts of IP addresses.\n(80 addresses, 160 addresses, &c.)')
