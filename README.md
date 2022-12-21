# tiktok-crawler
Crawl basic account info from https://www.tiktok.com/{account} and the details of recent posts.

## Deployment
There is a Dockerfile in branch: [build/docker](https://github.com/addie-tyc/tiktok-crawler/tree/build/docker) which can easily be deployed on cloud by container related services. e.g. Cloud Run
Please noted that there is a flask webserver wrapper because of the contract of Cloud Run:

> - Stateless (no volume attached to the container)
> - Answer to HTTP request

See [does-it-make-sense-to-run-a-non-web-application-on-cloud-run](https://stackoverflow.com/questions/62804653/) for more detail.
