# YouTube API Services — Audit form, project "noor-e-raah" (draft answers)

Draft for the owner to copy into the form by hand. This is a separate audit from Kissago's
(`docs/YOUTUBE_API_AUDIT_DRAFT.md`): another Google account, another Cloud project, another OAuth client.
No secrets here (no client secret, no token). Match each answer to the closest field in the live form and fill the
`<<...>>` placeholders yourself.

Until this audit passes, the project is unverified: every upload stays **private** and the owner makes it public /
schedules it in Studio (STUDIO ACTION message; `channels/noor-e-raah/channel.json` `"api_audited": false`).
After it passes: set `"api_audited": true` and the uploader sets public / publishAt itself.

Facts used:
- Google account: nooreraahofficial@gmail.com (owns the Cloud project and the channel)
- Google Cloud project: "noor-e-raah" — project number `<<Cloud console > Project info>>`
- OAuth client: Desktop app; app name "Noor-e-Raah Uploader"; status In production (unverified)
- Scopes: `youtube.upload`, `youtube`, `youtube.force-ssl`
- Home page: https://shamim8426.github.io/noor-e-raah-site/
- Privacy policy: https://shamim8426.github.io/noor-e-raah-site/privacy.html
- Terms of service: https://shamim8426.github.io/noor-e-raah-site/terms.html
- Channel: नूर-ए-राह | Noor-e-Raah, `UCmw4fs9jN49GTq7wVSdYm6w` (https://www.youtube.com/@NoorERaahHindi)

---

## 1. Contact / organisation

| Field | Answer |
|---|---|
| Name | `<<your full name>>` |
| Email | nooreraahofficial@gmail.com |
| Organisation | Individual creator (no company) — "Noor-e-Raah" |
| Address | `<<your postal address>>` |
| Website | https://shamim8426.github.io/noor-e-raah-site/ |
| Role | Owner of the channel and sole developer/operator of the API client |

## 2. API client

| Field | Answer |
|---|---|
| API client name | Noor-e-Raah Uploader |
| Project number | `<<project number>>` |
| Type | Private command-line tool (Python) running on the owner's own computer. Not a website, not a mobile app, not offered to anyone else. |
| Link to the API client | None — it is not public. Home page, privacy policy, terms and a screencast are provided instead. |
| Who uses it | Only the channel owner. One Google account, one channel. No third-party users and no end-user sign-up. |
| Number of users | 1 |

**Describe your API client and how it uses YouTube API Services**

> Noor-e-Raah Uploader is a private internal tool that I use to publish my own original Hindi story videos to my own
> YouTube channel "नूर-ए-राह | Noor-e-Raah" (UCmw4fs9jN49GTq7wVSdYm6w). I produce every video myself; the tool only
> uploads, schedules and organises the finished files and posts one comment of my own on my own videos.
>
> For each finished video it: (1) checks that the logged-in channel is exactly the expected channel
> (channels.list, mine=true) and stops if it is not; (2) uploads the video as private (videos.insert, with
> selfDeclaredMadeForKids and containsSyntheticMedia set explicitly); (3) makes it public or sets a publish time
> (videos.update, status only); (4) sets my custom thumbnail (thumbnails.set); (5) uploads my own Hindi subtitle file
> (captions.insert); (6) adds the video to one of my playlists (playlists.insert / playlistItems.insert); (7) posts one
> first comment of my own on my own video, e.g. a link from a Short to the full video (commentThreads.insert).
>
> It never reads, stores or displays data of other users or other channels, never deletes or edits other people's
> content, and never comments on other channels. The only data stored is the OAuth token for my own account, kept on
> my own computer.

**Which API features / endpoints**

| Endpoint | Why | Units each* |
|---|---|---|
| channels.list (mine) | safety check: correct channel before any write | 1 |
| videos.insert | upload my finished video (private) | 1,600 |
| videos.list (my own video IDs) | read my video's status before an update / comment | 1 |
| videos.update (status) | make my video public / set publishAt; or back to private | 50 |
| thumbnails.set | my custom thumbnail | 50 |
| captions.insert | my Hindi .srt subtitles | 400 |
| playlists.insert / playlistItems.insert | my own playlists | 50 |
| commentThreads.insert | one first comment of my own on my own video | 50 |

\*From the YouTube Data API quota table; confirm the current numbers in the quota calculator before submitting.

**Why these scopes**

> `youtube.upload` — videos.insert. `youtube` — playlists and video status on my own channel.
> `youtube.force-ssl` — captions.insert and commentThreads.insert (these endpoints require it).

**Does the client display YouTube data to users? Store it?**

> No display: there are no other users. Stored data: only the OAuth token for my own channel and, per upload, a
> small local JSON file with my own video's ID and URLs (for my records and to avoid duplicate uploads). Nothing is
> shared, sold or sent anywhere except to YouTube. No cookies, no analytics.

**Data deletion / revoking access**

> Access can be revoked at https://myaccount.google.com/permissions; deleting the local token file removes all stored
> credentials. No other data is kept.

**Do you comply with the YouTube API Services Terms of Service and Developer Policies?**

> Yes. The tool only acts on my own channel with my own authorisation, uploads only content I created and hold the
> rights to (or properly licensed music with attribution in the description), sets the made-for-kids and
> altered/synthetic-content declarations explicitly for every upload, and follows the privacy policy linked above.

**Privacy policy / Terms of service URL**

> Privacy policy: https://shamim8426.github.io/noor-e-raah-site/privacy.html
> Terms of service: https://shamim8426.github.io/noor-e-raah-site/terms.html

**Screencast / screenshots** (the form usually asks for a demo)

> `<<upload a short screen recording>>`: show (1) `python tools/youtube_upload.py --job <upload.json> --dry-run` and
> its summary, (2) the browser OAuth consent screen with the three scopes for "Noor-e-Raah Uploader", (3) a real
> upload finishing with "Channel OK: नूर-ए-राह | Noor-e-Raah", and (4) the video in YouTube Studio.
> Do not show `secrets/noor-e-raah/` (client secret, token).

## 3. Quota extension

| Field | Answer |
|---|---|
| Current quota | 10,000 units/day (default) |
| Requested quota | **10,000 units/day (no extension)** — or 20,000 if you want headroom |

> One upload with all extras uses about 2,250 units (videos.insert 1,600 + captions.insert 400 + thumbnails.set 50 +
> videos.update 50 + playlistItems.insert 50 + commentThreads.insert 50 + list calls). The plan is one long video and
> one Short per day = about 4,500 units, which fits the default. If you ask for 20,000: "headroom for retries of failed
> thumbnail/caption calls and an occasional re-upload; all calls are made by me, for my own content."

## 4. Before you submit (checklist)

- [ ] Project number filled; name and address filled.
- [ ] All three pages open in a private browser window (HTTP 200 checked on 2026-10-24).
- [ ] OAuth consent screen (Branding) has the same three links and authorized domain `shamim8426.github.io`.
- [ ] Screencast recorded without secrets on screen.
- [ ] Quota numbers checked against the current quota calculator.
- [ ] Submit while signed in as nooreraahofficial@gmail.com (the account that owns project "noor-e-raah").
