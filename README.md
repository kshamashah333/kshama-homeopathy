# Kshama Health & Homeopathy website

Single-page static site, served by GitHub Pages from `index.html`.

## Editing
Edit text and markup directly in `index.html`. If you add or change Tailwind classes or the inline script, rebuild:

    cd build && npm i tailwindcss@3.4.17 && python3 build.py ../index.html ../index.html

The build compiles Tailwind CSS into the page and rewrites the Content-Security-Policy hash for the inline script.

## Booking
Appointment booking uses Google Calendar appointment schedules. The links are in the `BOOKING` object near the end of `index.html`.
