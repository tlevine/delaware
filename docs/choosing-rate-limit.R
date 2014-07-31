N <- 8e6
ip.addresses <- 10 * 2^(3:6)
daily.quota <- seq(50, 4000, 50)

ymax <- 200

png('choosing-rate-limit.png', width = 1600, height = 900, pointsize = 24)
plot(0, 0, main = 'What should the rate limit be for the Delaware corporates scraper?',
     sub = '(Different lines are for different amounts of IP addresses.)',
     xlab = 'Number of requests that one worker makes per day',
     xlim = c(0, max(daily.quota) * 9/8),
     ylab = 'How many months to download all the data',
     ylim = c(0, ymax),
     type = 'n', bty = 'n', axes = F
)
axis(1)
axis(2, at = ((0:6)/12) * 365, labels = 0:6, las = 1)
abline(h = 0)

color <- 1
for (i in ip.addresses) {
    y <- 2*N/(i*daily.quota)
    lines(y ~ daily.quota, col = color)
    color <- color + 1
}
text(max(daily.quota), 2*N/(ip.addresses * max(daily.quota)),
     label = paste(ip.addresses, 'addresses'), pos = 4)
dev.off()
