# YouTube API Services — Audit and Quota Extension Form (draft answers)

Draft for the owner to copy into the form by hand. No secrets here (no client secret, no token).
Form fields change from time to time: match each answer below to the closest field in the live form, and fill the
`<<...>>` placeholders yourself.

Facts used (from `docs/YOUTUBE_UPLOADER_SETUP.md`):
- Google Cloud project: "Default Gemini Project" — project number `<<from Cloud console > Project info>>`
- OAuth client: Desktop app "story-channel-uploader"; app name "Dadi Ki Kahaniyan Uploader"; status In production (unverified)
- Scopes: `youtube.upload`, `youtube.force-ssl`
- Privacy policy: https://gist.github.com/shamim8426/9fdc382c9ac9a02777195c7c5969a1b6
- Channel today: किस्सागो | Kissago (formerly दादी की कहानियाँ), `UCy071_4g4vGemktFHybqkhQ`

---

## 1. Contact / organisation

| Field | Answer |
|---|---|
| Name | `<<your full name>>` |
| Email | shamimx.ali@gmail.com |
| Organisation | Individual creator (no company) — "Kissago" |
| Address | `<<your postal address>>` |
| Website | https://www.youtube.com/channel/UCy071_4g4vGemktFHybqkhQ |
| Role | Owner of the channel(s) and sole developer/operator of the API client |

## 2. API client

| Field | Answer |
|---|---|
| API client name | Dadi Ki Kahaniyan Uploader |
| Project number | `<<project number>>` |
| Type | Private command-line tool (Python) running on the owner's own computer. Not a website, not a mobile app, not offered to anyone else. |
| Link to the API client | None — it is not public. Description, privacy policy and a screencast are provided instead. |
| Who uses it | Only the channel owner. One Google account. No third-party users and no end-user sign-up. |
| Number of users | 1 |

**Describe your API client and how it uses YouTube API Services**

> Dadi Ki Kahaniyan Uploader is a private internal tool that I use to publish my own original animated Hindi story
> videos to my own YouTube channels. I write and produce every video myself; the tool only uploads and schedules the
> finished files.
>
> For each finished video it: (1) checks that the logged-in channel is the expected channel (channels.list, mine=true)
> and stops if it is not; (2) uploads the video as private with a scheduled publish time (videos.insert with
> status.publishAt, selfDeclaredMadeForKids and containsSyntheticMedia set explicitly); (3) sets my custom thumbnail
> (thumbnails.set); (4) uploads my own Hindi subtitle file (captions.insert); (5) optionally adds the video to one of my
> playlists (playlistItems.insert).
>
> It never reads, stores or displays data from other users or other channels, never deletes or edits other content,
> and never posts comments. The only data stored is the OAuth token for my own account, kept on my own computer.
> Today it serves one channel (UCy071_4g4vGemktFHybqkhQ); I plan to add more of my own channels (about 10), each
> authorised separately by me with its own token.

**Which API features / endpoints**

| Endpoint | Why | Units each* |
|---|---|---|
| videos.insert | upload my finished video, private + publishAt | 1,600 |
| thumbnails.set | my custom thumbnail | 50 |
| captions.insert | my Hindi .srt subtitles | 400 |
| playlistItems.insert | add to my playlist (optional) | 50 |
| channels.list (mine) | safety check: correct channel before upload | 1 |

\*From the YouTube Data API quota table; confirm the current numbers in the quota calculator before submitting.

**Does the client display YouTube data to users? Store it?**

> No display: there are no other users. Stored data: only the OAuth token for my own channel(s) and, per upload, a
> small local JSON file with my own video's ID and URLs (for my records and to avoid duplicate uploads). Nothing is
> shared, sold or sent anywhere except to YouTube.

**Data deletion / revoking access**

> I can revoke access at https://myaccount.google.com/permissions; deleting the local token file removes all stored
> credentials. No other data is kept.

**Do you comply with the YouTube API Services Terms of Service and Developer Policies?**

> Yes. The tool only acts on my own channels with my own authorisation, uploads only content I created and hold the
> rights to (or properly licensed music with attribution in the description), sets the made-for-kids and
> altered/synthetic-content declarations explicitly for every upload, and follows the privacy policy linked above.

**Privacy policy / Terms of service URL**

> Privacy policy: https://gist.github.com/shamim8426/9fdc382c9ac9a02777195c7c5969a1b6
> Terms of service: `<<none yet — if the form requires one, ask Claude Code to draft a short ToS gist>>`

**Screencast / screenshots** (the form usually asks for a demo)

> `<<upload a short screen recording>>`: show (1) running the dry-run command and its summary, (2) the browser OAuth
> consent screen with the two scopes, (3) a real upload finishing with "Channel OK", and (4) the video in YouTube
> Studio as Scheduled. Do not show the client secret or token files.

## 3. Quota extension

| Field | Answer |
|---|---|
| Current quota | 10,000 units/day (default) |
| Requested quota | **30,000 units/day** |

**Why do you need more quota?**

> Each upload uses about 2,101 units (videos.insert 1,600 + captions.insert 400 + thumbnails.set 50 +
> playlistItems.insert 50 + channels.list 1). The default 10,000 units allow only 4 uploads a day. I publish to my own
> channels (one now, about 10 planned) and expect 6–10 uploads per day in total (long videos and Shorts):
> 10 × 2,101 = 21,010 units. 30,000 units gives headroom for retries of failed thumbnail/caption calls and an
> occasional re-upload after a failed attempt. All calls are made by me, for my own content; there are no other users.

> Note for the owner: this assumes 6–10 uploads per day across all channels. If you mean 6–10 per channel per day
> (60–100 a day), ask for about 220,000 units/day and say so in the answer above.

## 4. Before you submit (checklist)

- [ ] Project number filled; name and address filled.
- [ ] Privacy policy gist opens in a private browser window.
- [ ] Screencast recorded without secrets on screen.
- [ ] Quota numbers checked against the current quota calculator.
- [ ] Same Google account (shamimx.ali@gmail.com) that owns the Cloud project submits the form.
