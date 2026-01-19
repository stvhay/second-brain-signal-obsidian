# Notes

**this is not secured by anything so definitely don't run it on public facing server. meant for internal communication only**


```bash
uv run signal-messages.py wss://endpoint/v1/receive/$number
```

**messages coming in**
```
2026-01-19 11:13:26,575 - INFO - Received: {"envelope":{"source":"+17032205356","sourceNumber":"+17032205356","sourceUuid":"81b9cfd8-5074-4dee-8385-d1087bdb48c3","sourceName":"Steve Hay","sourceDevice":1,"timestamp":1768839206488,"serverReceivedTimestamp":1768839206544,"serverDeliveredTimestamp":1768839206546,"syncMessage":{"sentMessage":{"destination":"+17032205356","destinationNumber":"+17032205356","destinationUuid":"81b9cfd8-5074-4dee-8385-d1087bdb48c3","timestamp":1768839206488,"message":"Foo","expiresInSeconds":0,"isExpirationUpdate":false,"viewOnce":false}}},"account":"+17032205356"}
2026-01-19 11:13:53,199 - INFO - Received: {"envelope":{"source":"+17032205356","sourceNumber":"+17032205356","sourceUuid":"81b9cfd8-5074-4dee-8385-d1087bdb48c3","sourceName":"Steve Hay","sourceDevice":1,"timestamp":1768839233154,"serverReceivedTimestamp":1768839233166,"serverDeliveredTimestamp":1768839233168,"syncMessage":{}},"account":"+17032205356"}

2026-01-19 11:14:39,689 - INFO - Received: {"envelope":{"source":"+17032205356","sourceNumber":"+17032205356","sourceUuid":"81b9cfd8-5074-4dee-8385-d1087bdb48c3","sourceName":"Steve Hay","sourceDevice":1,"timestamp":1768839279628,"serverReceivedTimestamp":1768839279660,"serverDeliveredTimestamp":1768839279661,"syncMessage":{}},"account":"+17032205356"}
2026-01-19 11:15:22,288 - INFO - Received: {"envelope":{"source":"+17032205356","sourceNumber":"+17032205356","sourceUuid":"81b9cfd8-5074-4dee-8385-d1087bdb48c3","sourceName":"Steve Hay","sourceDevice":1,"timestamp":1768839322143,"serverReceivedTimestamp":1768839322241,"serverDeliveredTimestamp":1768839322242,"syncMessage":{"sentMessage":{"destination":"+16178691278","destinationNumber":"+16178691278","destinationUuid":"f369fa48-ab4e-4265-9a74-5d53f7c1e00b","timestamp":1768839322143,"message":"Home server can now see my signal messages","expiresInSeconds":0,"isExpirationUpdate":false,"viewOnce":false}}},"account":"+17032205356"}
2026-01-19 11:15:35,794 - INFO - Received: {"envelope":{"source":"+16178691278","sourceNumber":"+16178691278","sourceUuid":"f369fa48-ab4e-4265-9a74-5d53f7c1e00b","sourceName":"Nate Costello","sourceDevice":1,"timestamp":1768839332329,"serverReceivedTimestamp":1768839335749,"serverDeliveredTimestamp":1768839335750,"receiptMessage":{"when":1768839332329,"isDelivery":true,"isRead":false,"isViewed":false,"timestamps":[1768839322143]}},"account":"+17032205356"}
2026-01-19 11:16:09,654 - INFO - Received: {"envelope":{"source":"+17032205356","sourceNumber":"+17032205356","sourceUuid":"81b9cfd8-5074-4dee-8385-d1087bdb48c3","sourceName":"Steve Hay","sourceDevice":1,"timestamp":1768839368751,"serverReceivedTimestamp":1768839369385,"serverDeliveredTimestamp":1768839369386,"syncMessage":{"sentMessage":{"destination":"+16178691278","destinationNumber":"+16178691278","destinationUuid":"f369fa48-ab4e-4265-9a74-5d53f7c1e00b","timestamp":1768839368751,"message":"This is how I can send notes to myself","expiresInSeconds":0,"isExpirationUpdate":false,"viewOnce":false,"attachments":[{"contentType":"image/jpeg","filename":"signal-2026-01-19-111608.jpeg","id":"8Qtv5bL6lWBxRKvFvSbb.jpeg","size":539384,"width":2048,"height":1152,"caption":null,"uploadTimestamp":1768839368829}]}}},"account":"+17032205356"}
2026-01-19 11:16:23,218 - INFO - Received: {"envelope":{"source":"+16178691278","sourceNumber":"+16178691278","sourceUuid":"f369fa48-ab4e-4265-9a74-5d53f7c1e00b","sourceName":"Nate Costello","sourceDevice":1,"timestamp":1768839379598,"serverReceivedTimestamp":1768839383209,"serverDeliveredTimestamp":1768839383212,"receiptMessage":{"when":1768839379598,"isDelivery":true,"isRead":false,"isViewed":false,"timestamps":[1768839368751]}},"account":"+17032205356"}
2026-01-19 11:16:35,412 - INFO - Received: {"envelope":{"source":"+17032205356","sourceNumber":"+17032205356","sourceUuid":"81b9cfd8-5074-4dee-8385-d1087bdb48c3","sourceName":"Steve Hay","sourceDevice":1,"timestamp":1768839395362,"serverReceivedTimestamp":1768839395392,"serverDeliveredTimestamp":1768839395393,"syncMessage":{}},"account":"+17032205356"}
2026-01-19 11:23:53,588 - INFO - Received: {"envelope":{"source":"+16178691278","sourceNumber":"+16178691278","sourceUuid":"f369fa48-ab4e-4265-9a74-5d53f7c1e00b","sourceName":"Nate Costello","sourceDevice":2,"timestamp":1768839831995,"serverReceivedTimestamp":1768839833539,"serverDeliveredTimestamp":1768839833564,"receiptMessage":{"when":1768839831995,"isDelivery":true,"isRead":false,"isViewed":false,"timestamps":[1768839322143,1768839368751]}},"account":"+17032205356"}`/`
```

**example curl send simple message**

```bash
curl -SsL -X POST      -H "Content-Type: application/json"      -d '{ "message": "test send 1", "number": "+17032205356", "recipients": ["+17032205356"]}'      http://signal-bot.st5ve.duckdns.org/v2/send

{"timestamp":"1768838572087"}
```

**link signal-bot to existing account**

```bash
curl -X GET -H "Content-Type: application/json" 'http://signal-bot/v1/qrcodelink?device_name=signal-bot'
```

returns a qrcode image. can run in browser for example.

**using nginx proxy manager npm**

- restrict access to VPN only.
- turn off auto upgrade https and use this custom directive.

```
# Use 308 instead of 301/302 - preserves POST method
if ($scheme != "https") {
    return 307 https://$host$request_uri;
}
```

- turn on websockets
- turn on http/2
