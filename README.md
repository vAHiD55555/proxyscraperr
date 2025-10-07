# GitLab proxy automation

این پروژه شامل همهٔ فایل‌های لازم است تا:
- هر ساعت پروکسی‌ها از منابع مشخص خوانده و تست شوند
- پروکسی‌های زنده در `alive_proxies.txt` ذخیره شوند
- رشتهٔ هگز تولید شده در `proxy.pac` قرار گیرد
- در صورت تنظیم متغیرهای CI، `proxy.pac` و `alive_proxies.txt` به‌صورت خودکار در ریپو کامیت شوند

فایل‌های داخل بسته:
- .gitlab-ci.yml
- proxy_check.py
- proxy.pac.template
- encode_proxies.py
- README.md

دستورالعمل سریع:
1. فایل‌ها را در ریشهٔ ریپوی GitLab قرار بده.
2. در GitLab → Settings → CI/CD → Variables مقدارهای زیر را قرار بده:
   - GITLAB_USER = نام کاربری گیت‌لب
   - GITLAB_TOKEN = Personal Access Token (scopes: write_repository)
3. در GitLab → CI/CD → Schedules یک برنامهٔ جدید با Cron: `0 * * * *` ایجاد کن.
4. برای تست محلی در ترمکس:
   - `python proxy_check.py`
   - خروجی `alive_proxies.txt` را بررسی کن
   - `python encode_proxies.py` خروجی هگز را چاپ می‌کند؛ آن را در `proxy.pac.template` جایگزین کن یا صبر کن CI خودش انجام دهد.

توجه: توکن را در فایل‌ها قرار نده؛ از CI Variables استفاده کن.
