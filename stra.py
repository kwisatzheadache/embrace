walk_input = dire
angle = 15

rotation = (.72*angle)/360
if isinstance(walk_input, str):
    walks = stack_walks(walk_input)
else:
    walks = walk_input
df = pd.DataFrame(walks[100:])
mag_z = walks[:,9]
lagged = lag(mag_z, 100)
straight = []
for i in range(len(lagged)):
    avg = np.mean(lagged[i])
    low = avg - rotation
    high = avg + rotation
    if all(low <= j <= high for j in lagged[i]):
        straight.append(df.iloc[[i]])
np.array(straight)
