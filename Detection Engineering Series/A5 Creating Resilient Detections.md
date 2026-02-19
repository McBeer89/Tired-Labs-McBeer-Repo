# Creating Resilient Detections

**Author:** VanVleet  
**Published:** November 13, 2024  
**Reading Time:** 12 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

<!-- Image: Article header image - not accessible -->

I've spent a lot of time focusing on higher-level [threat detection strategy](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62), but today I'm going to take a detour to talk at a more tactical level: how to create detections that are resilient to common SIEM problems like ingest lag and query failure. Today I'll talk about some common problems and share some best practices for making your detections more resilient, and hopefully save you some future grief!

It is very frustrating to have built the perfect detection, but when the moment comes for it to shine something goes wrong and the event goes by undetected. So let's talk about the kinds of failures we commonly see and what options we have for building in resilience.

## Ingest Delay Resilience

This is both the most common and easiest problem to solve, so it's a great place to start! As a side note, I am by no means the first [person](https://learn.microsoft.com/en-us/azure/sentinel/ingestion-delay) to [discuss](https://cybermsi.com/blog/security/implementing-ingestion-delay-correction-in-microsoft-sentinel/) [this](https://community.splunk.com/t5/Luxembourg-User-Group/Developing-reliable-searches-dealing-with-events-indexing-delay/m-p/665588) [problem](https://www.databricks.com/blog/cybersecurity-lakehouses-part-2-handling-ingestion-delays), but awareness of the issue in the Detection Engineering community seems low and most of the solutions I find online only partly solve the problem. So, I'll spill a little more ink in the hopes of raising awareness and offering a better solution.

Let's begin by defining some terms and concepts:

* **Ingest delay** is the time difference between when an event actually happens and when the log recording that event gets ingested into your SIEM.
* Every detection automation platform I've ever seen involves running a query on a recurring schedule with a defined **lookback window**, which is the window of time that each query execution will inspect. Typically, queries will run hourly or every 30 minutes and look back the same amount of time. This sliding window ensures that every log gets inspected in turn without overlap (which could cause duplicate alerts). Lookback windows can be **immediate** (the time window starts at query time and looks back X minutes) or **delayed** (the time window starts at query time minus some predetermined period and looks back X minutes).
* Whenever a record is ingested into a database or document store, there are two timestamps you should know about: the **event time** is the time that the event actually happened, and the **ingest time** is the time when the log recording that event was ingested into the database. In security, almost every query is time-bounded, and the event time is almost always what's used. (Most out-of-the-box detections and SIEMs I've seen use event time.)

Visualizing this, a 30 minute recurring query with a 30 minute immediate lookback window (using event time) would look like this:

<!-- Image: Timeline diagram showing query executing on 30 minute schedule with 30 minute lookback window -->

Query on 30 minute schedule with a 30 minute lookback window

The problem with ingest lag arises when logs aren't in the SIEM at the point that your detection query is looking for them. Imagine you have a query that is running every 30 minutes, and the log you need to detect a malicious event is delayed by 30 minutes. When your query runs and looks back 30 minutes, the log is not present in the SIEM, so you don't get an alert. But, when the next query runs in 30 minutes, the lookback window has adjusted forward and no longer includes the time when the event happened! Your detection might be 100% capable of detecting the malicious activity, but you miss it because of the ingest lag.

<!-- Image: Timeline diagram showing a missed event that falls into the gap caused by ingest lag -->

A missed event caused by ingest lag

I've never met a SIEM that is actually real-time, so some ingest lag is always present. **If you're using the event time as your query timestamp and an immediate lookback window, you probably have a blind spot.** There are events that would fall in your query window, but haven't been ingested yet. The size of your blind spot will depend on the log source's ingest delay and length of your lookback window, but it's almost certain there is at least a small one! If that critical event happens to occur in the blind spot, you're going to miss it.

Here's how to find out how big your blind spot is: run a query in your SIEM using your typical detection query lookback period, and count the number of records in each 2 minute window. Let's graph it to make it easier to see. You'll likely see a point where the graph begins to slide downhill. That downward slope, plus any totally empty bins, are your detection's ingest delay blind spot.

<!-- Image: Graph showing event count over one hour lookback window with average ingest delay of 30 minutes - shows declining count toward the present -->

Graph of a one hour lookback window on a log source with an average ingest delay of 30 minutes.

If a graph of your log source looks like this and you're using an event time as your detection query timestamp, you have a blind spot. **Remember that even though those logs in the blind spot will get ingested later, they'll never fall inside the query's sliding time window again! Each execution of the query is going to have its blind spot, reducing the chances that your detection will find the specific log(s) it's looking for.**

Even a log with an impressively low lag time will still have a blind spot.

<!-- Image: Graph showing event count over one hour lookback window with average ingest delay of 3 minutes - shows small decline toward the present -->

Graph of a one hour lookback window on a log source with an average ingest delay of 3 minutes.

And in a worst case scenario where the ingest lag is almost as long as your lookback window, your blind spot might be pretty close to a total eclipse!

<!-- Image: Graph showing event count over 30 minute lookback window with average ingest delay of 30 minutes - shows significant blind spot -->

Graph of a 30 minute lookback window on a log source with an average ingest delay of 30 minutes.

Hopefully you're already familiar with your SIEM's normal ingest lag time and you've planned for it. One solution is to use a delayed lookback window that is greater than your longest expected ingest lag (not the average lag!). This allows enough time that events **should** be ingested before you query a given time window.

<!-- Image: Timeline diagram showing query with 30 minute delayed lookback window -->

Query with a delayed lookback window of 30 minutes.

The trade-off with this approach is that your 'time to detect' (the length of time from a malicious event to when you know it happened) is also delayed. In our example above, the delayed lookback provides resilience to ingest delays up to 30 minutes, but your alert on a malicious event is also delayed 30 minutes (regardless of the current ingest delay). But at least you shouldn't have a blind spot, so you can be confident you'll actually get an alert!

**The real challenge with ingest lag is when there are unexpected surges.** An ingest lag that suddenly climbs to two or four hours (or worse!) will almost certainly exceed any delayed lookback, resulting in possible detection misses. And what happens if ingest completely stops for 6 hours while the engineering team finds and fixes the problem? Even if they eventually get all the delayed logs ingested, your query windows will have passed and you'll have missed any alerts that would have fired during the downtime.

**The best solution for resilience to ingest lag is to use the ingest time instead of the event time in your detection queries.** Using an ingestion-based timestamp means that all events are guaranteed to be inspected by your detection query **in the next query after they are ingested**, regardless of how much ingest lag you're experiencing. Even if the SIEM is down for a full day, as long as the delayed logs are eventually ingested, they'll be inspected in the very next query execution. No missed alerts, just delayed ones. Using an ingest timestamp also means you don't have to use a delayed lookback window, so there are no built-in detection delays. You have the lowest time-to-detect possible, whatever the current ingest delay. That's resilience! :)

> Note: In order to make testing for an ingest delay blind spot easier, I've included a simple PowerShell script at the end of this article.

### Using Ingest Time in your SIEM

In my experience, most SIEMs use event time as the primary timestamp (it would mess up other searching use cases to use the ingest time as the primary timestamp) and their automated queries use the primary timestamp by default. So, if you're using the defaults you probably have at least a small ingest delay blind spot. Hopefully, though, your SIEM makes it possible to use an ingest timestamp instead. Here are a few I've worked with:

* Azure Data eXplorer (ADX — which I'm becoming a big fan of!) makes it very easy to use ingest time. The ADX API doesn't define separate parameters for query times, they have to be provided in the query itself. So, you have full control of the time parameters and can just use the ingestion\_time() function, and you're done! Of course, ADX also doesn't provide automated queries, so you have to figure that part out yourself!
* Sentinel's Analytics Rules and Splunk's Alerts both automatically query against the event time, but there are a couple of workarounds available. Microsoft suggests [a limited one](https://learn.microsoft.com/en-us/azure/sentinel/ingestion-delay) (it is only resilient up to the anticipated ingest delay, any longer and you will miss events), and Splunk suggests a [better one](https://docs.splunk.com/Documentation/SCS/current/Search/Timemodifiers#Searching_based_on_index_time) (but it's still a hack that requires you to knowingly use it!). Splunk's solution works for both platforms, so I'll summarize it here. Add a clause to your query to select on ingestion time: in Splunk, use the \_index\_earliest and \_index\_latest fields, in Sentinel use the ingestion\_time() function. You can see examples of each in the links above. Make sure you define the time dynamically: -1h in Splunk and ago(1h) in Sentinel. Then set the query lookback (which uses event time) as far as the platform will allow ("All Time" for Splunk and the last 14 days for Sentinel).\* This means the event time-based clause will not play a meaningful role in selecting records, so your ingest time clause becomes the primary time-based filter.
* ElasticSearch, if you're using the API directly, allows you to specify any timestamp in your query's range statement. You do have to [add ingest time](https://discuss.elastic.co/t/how-to-add-time-of-ingestion-to-the-document/243042) to records in your ingest pipeline, since it's not added by default. In the Elastic Common Schema, the ingest time should be named event.ingested, so use that and you're set.
* I've never used Splunk Enterprise Security or Elastic Security (Splunk and Elastic's SIEM offerings), so if you know how to use ingest time in your automated queries on those platforms, post a comment below and share the knowledge! I'm guessing you could get Splunk's workaround to work in either platform.

You'll have to figure out the best solution for your environment, given your SIEM and ingest delays (don't forget to think about normal delays and potential surges!). If your SIEM doesn't support using ingest times for automated queries, it's time to put in a feature request! Also, at the end of this article is a script you can use to verify your solution is working.

\* Allow me to debunk something I saw in multiple articles talking about Microsoft's solution: the idea that setting the maximum lookback window means a less efficient query. This is a misunderstanding of what this query is doing. The ingest time criteria limits the records searched in the same way an event time criteria would limit it; if you're using the same lookback window length for both the efficiency should be equivalent. You can see this for yourself in Splunk by running a search for "index=whatever | stats count" with "last 60 minutes" in the time picker. Then inspect the job and note how many records it scanned. Now, search "index=whatever \_index\_earliest=-60m \_index\_latest=now | stats count" with the time picker at "All Time" and inspect the job. The number of records scanned and time taken won't be drastically different. By setting a shorter event time lookback window, like in Microsoft's solution, you're just setting limitations on your ingest delay resilience: as soon as ingest delay exceeds your event time lookback, you start missing events. **There is no trade-off between ingest delay resilience and query efficiency when using an ingest timestamp properly.**

## Query Failure Resilience

Another source of detection misses is query platform failures. What might fail is platform specific, but any platform can have failed runs due to things like API rate limits, network failures, or platform downtime. If bad luck causes a malicious event to coincide with a failed query window, the event will be missed.

<!-- Image: Timeline diagram showing event missed due to query failure -->

Event missed due to query failure.

There are three options for addressing query failure misses. Unfortunately, the best options require support from your detection automation platform, so if your platform doesn't support any of these, it's time to put in a feature request!

### Option 1: Health monitoring and manual/automated resubmission

For this option, you configure notifications for any failed queries, and then you re-run any failed queries to ensure no malicious events were missed. This can be done manually or automatically, but automatic resubmission is definitely superior. It could be difficult to re-run all detections manually if you have hundreds or thousands of them. Ideally, this solution would be automated so that a failed query is resubmitted to cover the missed timeframe. Even more ideally, this automated failure detection and resubmission would be implemented by your detection automation platform, so you don't have to worry about it at all!

### Option 2: Overlapping Lookback Windows

You can build in some failure resilience by configuring your detection queries to use overlapping lookback windows. Then, if one query fails, a subsequent query will still cover the failed query window and you won't miss any events. Your failure resilience will be equal to the number of overlapping windows, but consecutive query failures will result in missed alerts. For example, you could use a 30-minute recurring query with a 1 hour lookback window, and this would provide resilience for a single failure. Two consecutive failures would leave a missed query window.

<!-- Image: Timeline diagram showing query on 30 minute schedule with 1 hour overlapping lookback window -->

Query on a 30 minute schedule with a 1 hour overlapping lookback window.

This approach requires some method for deduplicating alerts because under normal circumstances a given malicious event will be inspected in multiple executions of the detection query. It also can cause some hiccups with event grouping: if you deduplicate AFTER you've grouped events, then a subsequent query execution might find a slightly different set of events (because some of them might fall outside the new lookback window) and generate a duplicate alert. All told, this solution can work, but it definitely can cause its share of headaches. I prefer options 1 and 3.

<!-- Image: Timeline diagram showing duplicated alert caused by grouping events on different windows -->

Duplicated alert caused by grouping events on different windows.

### Option 3: Adjusted Query Lookback

This option requires support from your detection automation platform, but it's a simple solution. In this solution the automation platform records the query window for each execution. When a query runs, the platform automatically adjusts the query window to cover the time between the last successful execution and the current time. No deduplication is required because each time window will be queried only once.

<!-- Image: Timeline diagram showing a failed query with adjusted lookback window for subsequent query execution -->

A failed query with an adjusted lookback window for the subsequent query execution.

## Conclusion

Hopefully this article has provided some useful ideas for how you can ensure your detections are as resilient as possible, so they'll work in the best of times and the worst of times (perhaps just a little delayed).

If you have any thoughts to add, please leave them in the comments below!

## Script for Measuring Your Ingest Delay Blind Spot

If you're concerned that you have an ingest delay blind spot, here is a simple PowerShell script to help quantify it. The script will spawn a cmd.exe process with a unique command line every 5 minutes for one hour, for a total of 12 instances. To use it, create a detection in your automation platform for a process command line containing the string "IngestDelayTestCommand." Set it to run at your normal recurrence frequency and with your typical lookback window. Then run this script on a machine that's logging to your SIEM and verify how many of the 12 possible alerts you actually get. Then ask yourself how many missed events is acceptable. (I know, I know… I'm leading the witness. 😁)
```powershell
#This script helps test for an ingest delay blind spot  
#To use it, create a detection in your automation platform that looks for "IngestDelayTestCommand" in a process command line.  
#Then run this script on an asset that is logging to your SIEM. The script will execute a cmd.exe process that echos the expected   
#string every 5 minutes for an hour. Your ingest delay blind spot is the number of alerts you DON'T get out of the 12 possible.  
  
for ($i=1; $i -le 12; $i++) {  
    $currenttime = Get-Date -Format "HH:mm:ss"  
    $command = 'echo {0} IngestDelayTestCommand - Test #{1}' -f $currenttime, $i  
    & cmd.exe /c $command  
    Start-Sleep -seconds 300  
}
```

Output will look like:
```
07:33:38 IngestDelayTestCommand - Test #1
```

And the command line will look like:
```
"C:\WINDOWS\system32\cmd.exe" /c "echo 09:13:06 IngestDelayTestCommand - Test #1"
```

---

**Tags:** Threat Detection, Resilience, Detection Engineering, Siem