library(ggplot2)
library(dplyr)

# Create DataFrame
top_tracks <- data.frame(
  Track = c("Nun id change", "Systëm", "German", "Wat it feel lykë", "1Take (Naija to London)",
            "stunning. - sped up", "We Don't Luv Em - Remix", "Duality", "BLACK OPS (with Denzel Curry)", "Menage - Guitar remix"),
  Popularity = c(68, 60, 59, 53, 45, 44, 44, 43, 42, 28)
)

# Bar Chart
ggplot(top_tracks, aes(x = reorder(Track, Popularity), y = Popularity, fill = Track)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  coord_flip() +
  labs(title = "Top 10 Most Listened-To Tracks", x = "Track", y = "Popularity") +
  theme_minimal()

top_albums <- data.frame(
  Album = c("AftërLyfe", "Lyfë", "Mind of a Gemini", "stunning.", "BLACK OPS"),
  Total_Tracks = c(22, 12, 7, 2, 1)
)

ggplot(top_albums, aes(x = reorder(Album, Total_Tracks), y = Total_Tracks, fill = Album)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  coord_flip() +
  labs(title = "Top 5 Albums by Number of Tracks", x = "Album", y = "Total Tracks") +
  theme_minimal()

avg_pop_artists <- data.frame(
  Artist = c("Yeat", "EO", "Mixtape Madness", "hako", "HoodRich Pablo Juan"),
  Avg_Popularity = c(60, 59, 45, 44, 44)
)

ggplot(avg_pop_artists, aes(x = reorder(Artist, Avg_Popularity), y = Avg_Popularity, fill = Artist)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  coord_flip() +
  labs(title = "Top 5 Artists by Average Track Popularity", x = "Artist", y = "Average Popularity") +
  theme_minimal()

track_durations <- data.frame(
  Track = c("1Take (Naija to London)", "stunning. - sped up"),
  Duration_MS = c(283898, 94899)
)

ggplot(track_durations, aes(x = Track, y = Duration_MS, fill = Track)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  labs(title = "Longest and Shortest Tracks", x = "Track", y = "Duration (ms)") +
  theme_minimal()

playlists <- data.frame(
  Playlist = c("New Lit", "Reg"),
  Total_Tracks = c(202, 124)
)

ggplot(playlists, aes(x = reorder(Playlist, Total_Tracks), y = Total_Tracks, fill = Playlist)) +
  geom_bar(stat = "identity", show.legend = FALSE) +
  coord_flip() +
  labs(title = "Top 5 Playlists by Number of Tracks", x = "Playlist", y = "Total Tracks") +
  theme_minimal()
