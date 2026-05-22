# Ignore With Reason Test

<!--- refcheck-ignore: this is a known false positive -->
[ignored_link](ignored.md)

[kept_link](kept.md)

<!--- refcheck-ignore-start: entire section produces false positives -->

[ignored_one](ignored1.md) [ignored_two](ignored2.md)

<!--- refcheck-ignore-end -->

[also_kept](also_kept.md)
