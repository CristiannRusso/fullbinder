# FullBinder — Concept

## What it is

FullBinder is a local desktop application for organizing important
personal documents: bills, contracts, receipts, certificates, medical records.

It runs entirely on the user's computer. No accounts, no cloud, no
synchronization. Documents stay under the control of their owner.

## Who it's for

The target user is a non-technical adult who:

- Mainly uses a computer for important matters (banking, email, documents).
- Already stores important documents on their PC, but struggles to find
  them when needed.
- Doesn't trust cloud services with sensitive documents — prefers
  to keep them on their own device.
- Can handle basic apps (clicking, saving, opening files) but not
  technical configuration (accounts, sync, permissions).

Real-world example: a parent who receives bills as PDFs via email,
signed contracts to scan, occasional medical certificates. Today,
these documents end up scattered across messy folders on the computer
and become hard to find.

## The problem it solves

People who manage important documents on their PC face three problems:

1. **Disorganization** — files end up scattered across Downloads,
   Documents, Desktop, email attachments. They get lost.
2. **Hard to search** — when a document is actually needed (last year's
   bill, a signed contract), finding it takes time and frustration.
3. **Forgotten deadlines** — insurance policies, contracts, certificates
   have expiration dates. Without reminders, they are discovered too late.

FullBinder solves organization, search, and deadlines while remaining
entirely local and requiring no technical skills.

## What it does (and what it doesn't)

### Does

- Organizes documents into binders by topic (e.g. "Home", "Health",
  "Car", "University"), like a physical ring binder.
- Lets the user upload files of any format (PDFs, images, docs).
- Tags, colors, and categories to identify binders at a glance.
- (Phase 3) Full-text search inside documents via OCR.
- (Phase 3) Reminders for important expiration dates.
- (Phase 3) Automatic backup to a ZIP file on a local folder or USB stick.
- (Phase 4) Distributed as a native desktop app (.app for Mac, .exe for
  Windows) — no terminal, no Python installation required.

### Does NOT (by design)

- No cloud, no sync between devices.
- No user accounts, no login, no passwords (in Phase 1).
- No sharing between users.
- No collaborative editing.
- No mobile app (the target user works on a computer).
- No replacement for Google Drive or Dropbox — it's a product for
  a different use case.

## Roadmap

- **Phase 1 (in progress)** — Working MVP: binders, documents, upload,
  download, edit, delete. Single-device, no encryption.
- **Phase 2** — Optional local encryption with passphrase (for users
  who want extra protection). To be evaluated based on real user needs.
- **Phase 3** — OCR for full-text document search, expiration reminders,
  automatic backup to ZIP.
- **Phase 4** — Desktop packaging (PyWebView + PyInstaller) for
  distribution as .app/.exe.

## Tech stack

- Backend: Python 3 + Flask + SQLAlchemy
- Database: SQLite (local file)
- Frontend: Jinja2 + custom CSS + vanilla JavaScript
- Future packaging: PyWebView + PyInstaller

## Philosophy

Personal data belongs to the user. FullBinder doesn't see it, doesn't
sync it, doesn't send it anywhere. It works offline, forever.