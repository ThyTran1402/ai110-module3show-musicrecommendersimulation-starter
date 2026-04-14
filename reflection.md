# Reflection: Comparing User Profiles

## Happy Pop Fan vs. Chill Lofi Listener

The Happy Pop Fan's top results cluster tightly around upbeat, high-energy pop tracks. The Chill Lofi Listener's results are quieter, slower, and mostly acoustic. The key driver of this difference is that both genre (+2.0) and energy similarity work in the same direction for each profile — the lofi listener's low target energy rewards low-energy songs, while the pop fan's high target energy rewards high-energy songs. When genre and energy both point the same way, the system produces very consistent, expected output.

## Chill Lofi Listener vs. High-Energy Metal Head

These two profiles are near-opposites on the energy axis (0.35 vs. 0.95). As a result, almost no song appears in both top-5 lists. The metal head's list contains songs with energy above 0.85; the lofi listener's list contains songs with energy below 0.45. This makes intuitive sense — the energy similarity term acts as a natural filter that keeps these profiles from converging.

## Happy Pop Fan vs. High-Energy Metal Head

Both profiles have high target energy (0.8 and 0.95), so their energy-driven rankings overlap somewhat — *Gym Hero* appears in both top-5 lists because it is an intense, high-energy pop song. The genre bonus separates them: the pop fan scores it at 2.87 (genre match), while the metal head scores it at 1.98 (mood match only). This shows that shared energy can create unexpected overlaps between very different listeners, which is a real limitation of simple energy-only scoring.

## Takeaway

The scoring system behaves predictably for "pure" profiles with consistent preferences, but the genre bonus is strong enough to override energy and mood signals in many cases. A listener who loves a genre that happens to be underrepresented in the catalog (like classical or metal) will receive less varied recommendations than a pop fan, simply because there are fewer genre matches available to earn those 2.0 points.
