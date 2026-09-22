# CSV Cleaner Studio

A small, dependency-free Python toolkit for **safe, reproducible CSV cleanup** from the command line or Python code.

> English documentation first · التوثيق العربي بالأسفل

## Overview
CSV files from spreadsheets, exports, and manual entry often contain whitespace, duplicate rows, inconsistent headers, empty rows, or unused columns. CSV Cleaner Studio handles those routine problems with explicit options and a machine-readable audit report. It never modifies the source file in place.

## Key features
- Detects comma, semicolon, tab, and pipe delimiters, or accepts an explicit delimiter.
- Trims cell whitespace and normalizes headers; duplicate header names become deterministic (`name`, `name_2`).
- Removes duplicate and fully empty rows by default.
- Optionally removes fully empty columns, selects/reorders columns, or drops named columns.
- Reads UTF-8 and UTF-8-BOM; writes deterministic UTF-8 CSV with `\n` line endings.
- Rejects malformed rows with inconsistent column counts instead of silently shifting data.
- Optional JSON report includes before/after counts and SHA-256 of the output.
- CLI, stdin/stdout pipelines, and reusable Python API. No runtime dependencies, network access, telemetry, or credentials.

## Preview
```console
$ csv-cleaner messy.csv -o clean.csv --drop-empty-columns --report report.json
Cleaned 124 -> 118 rows; 9 -> 8 columns.
```
For screenshots, capture the terminal command together with a small non-sensitive sample CSV and its report. The project is CLI-first and does not ship a graphical interface.

## Requirements & installation
Requires Python 3.10+.

```bash
git clone https://github.com/rad03i2/csv-cleaner-studio.git
cd csv-cleaner-studio
python -m pip install .
```
For development/tests:
```bash
python -m pip install -e . pytest
pytest
```

## Usage
```bash
csv-cleaner input.csv -o clean.csv
csv-cleaner input.csv -o clean.csv --drop-empty-columns --lowercase-headers
csv-cleaner input.csv -o clean.csv --select name,email,city
csv-cleaner input.csv -o clean.csv --drop internal_note --report report.json
cat input.csv | csv-cleaner - --stdout > clean.csv
python -m csv_cleaner input.csv -o clean.csv
csv-cleaner --version
```
Defaults: trim cells, normalize headers, deduplicate rows, and remove fully empty rows. Use `--no-trim`, `--no-normalize-headers`, `--keep-duplicates`, or `--keep-empty-rows` to disable them. `--delimiter ';'` bypasses delimiter detection. Column names passed to `--select`/`--drop` refer to the resulting normalized headers.

### Python API
```python
from csv_cleaner import CleanOptions, clean_file

report = clean_file(
    "raw.csv",
    "clean.csv",
    CleanOptions(drop_empty_columns=True, lowercase_headers=True),
)
print(report.to_dict())
```

## Project structure
```text
src/csv_cleaner/   core engine, CLI, public API
tests/             core and CLI tests
examples/          safe sample input
.github/workflows/ cross-platform CI
```

## Testing
`pytest` exercises delimiter detection, trimming, header normalization, deduplication, empty-row/column handling, column selection, validation, overwrite protection, hashing, and end-to-end CLI output. CI also compiles the package and runs the CLI version smoke test on Python 3.10, 3.12, and 3.13 across Linux, Windows, and macOS.

## Security & privacy
Processing is local. The tool does not execute CSV content, use formulas, access the network, or send telemetry. Output is written only to the requested path. Spreadsheet applications may interpret cells beginning with `=`, `+`, `-`, or `@` as formulas; this tool preserves cell content and **does not claim to sanitize CSV formula injection**. See `SECURITY.md`.

## Limitations
This is a deterministic CSV cleaner, not a spreadsheet engine or statistical data-imputation system. It supports UTF-8 input only, loads the CSV into memory, does not infer data types, and does not alter formula-like values. Delimiter sniffing is heuristic; use `--delimiter` when the format is known. Very large files may require a streaming tool.

## Optional roadmap
Potential future work: streaming mode, explicit encoding conversion, configurable null markers, and opt-in formula neutralization. These are not current features.

## Contributing
See `CONTRIBUTING.md`. Bug reports and focused improvements with tests are welcome.

## License
MIT License. See `LICENSE`.

## Author
**Radwan Abdulhadi Ahmed** · **رضوان عبدالهادي أحمد** · GitHub: **@rad03i2**

---

# العربية — CSV Cleaner Studio

أداة Python صغيرة وبدون اعتماديات تشغيل لتنظيف ملفات **CSV بصورة آمنة وقابلة للتكرار** من سطر الأوامر أو من كود Python.

## نظرة عامة ولماذا يوجد المشروع
ملفات CSV الناتجة من الجداول والتصدير والإدخال اليدوي كثيرًا ما تحتوي مسافات زائدة، وصفوفًا مكررة أو فارغة، وعناوين أعمدة غير متناسقة، وأعمدة غير مستخدمة. يعالج المشروع هذه المشكلات بخيارات صريحة ويستطيع إنشاء تقرير JSON للتدقيق، مع رفض تعديل ملف المصدر نفسه مباشرة.

## الميزات الرئيسية
- اكتشاف الفاصلة والفاصلة المنقوطة وTab و`|` تلقائيًا، مع إمكانية تحديد الفاصل يدويًا.
- إزالة المسافات وتطبيع أسماء الأعمدة وجعل الأسماء المكررة فريدة بصورة حتمية.
- حذف الصفوف المكررة والفارغة بالكامل افتراضيًا.
- حذف الأعمدة الفارغة اختياريًا، واختيار الأعمدة وترتيبها أو إسقاط أعمدة محددة.
- قراءة UTF-8 وUTF-8-BOM وكتابة UTF-8 ثابتة.
- رفض الصفوف ذات عدد الأعمدة غير المتناسق بدل تغيير البيانات بصمت.
- تقرير JSON اختياري يتضمن الأعداد قبل/بعد وبصمة SHA-256 للخرج.
- CLI وstdin/stdout وPython API، بدون شبكة أو telemetry أو مفاتيح سرية.

## المعاينة والتثبيت
المشروع موجّه للطرفية ولا يتضمن واجهة رسومية. يتطلب Python 3.10 أو أحدث.
```bash
git clone https://github.com/rad03i2/csv-cleaner-studio.git
cd csv-cleaner-studio
python -m pip install .
```
للتطوير والاختبارات:
```bash
python -m pip install -e . pytest
pytest
```

## الاستخدام
```bash
csv-cleaner input.csv -o clean.csv
csv-cleaner input.csv -o clean.csv --drop-empty-columns --report report.json
csv-cleaner input.csv -o clean.csv --select name,email,city
python -m csv_cleaner input.csv -o clean.csv
```
الإعدادات الافتراضية تنظف المسافات، وتطبع عناوين الأعمدة، وتحذف التكرار والصفوف الفارغة. يمكن تعطيلها بخيارات `--no-trim` و`--no-normalize-headers` و`--keep-duplicates` و`--keep-empty-rows`. أسماء `--select` و`--drop` تشير إلى أسماء الأعمدة بعد التطبيع.

### Python API
```python
from csv_cleaner import CleanOptions, clean_file
report = clean_file("raw.csv", "clean.csv", CleanOptions(drop_empty_columns=True))
print(report.to_dict())
```

## بنية المشروع والاختبار
`src/csv_cleaner/` للمحرك والـCLI والواجهة البرمجية، و`tests/` للاختبارات، و`examples/` للعينة الآمنة، و`.github/workflows/` للتكامل المستمر. تغطي الاختبارات اكتشاف الفاصل والتنظيف والتكرار والأعمدة والتحقق والحماية من الكتابة فوق المصدر والتقرير وسلوك CLI.

## الأمان والخصوصية
المعالجة محلية ولا تنفذ محتوى CSV ولا تتصل بالإنترنت. انتبه إلى أن برامج الجداول قد تفسر القيم التي تبدأ بـ`=` أو `+` أو `-` أو `@` كصيغ؛ الأداة تحافظ على محتوى الخلايا ولا تدّعي منع CSV formula injection. راجع `SECURITY.md`.

## القيود
ليست الأداة محرك جداول أو نظام تحليل إحصائي. تقبل UTF-8 فقط، وتحمل الملف في الذاكرة، ولا تستنتج أنواع البيانات ولا تغيّر القيم الشبيهة بالصيغ. اكتشاف الفاصل استدلالي؛ استخدم `--delimiter` عند معرفة التنسيق. الملفات الضخمة جدًا قد تحتاج أداة streaming.

## التطوير المستقبلي الاختياري
يمكن مستقبلًا إضافة وضع streaming وتحويل ترميزات صريح وعلامات null قابلة للضبط وتعطيل صيغ الجداول اختياريًا. هذه ليست ميزات حالية.

## المساهمة والترخيص
راجع `CONTRIBUTING.md` للمساهمة. المشروع مرخص برخصة MIT؛ راجع `LICENSE`.

## المؤلف
**Radwan Abdulhadi Ahmed** · **رضوان عبدالهادي أحمد** · GitHub: **@rad03i2**
