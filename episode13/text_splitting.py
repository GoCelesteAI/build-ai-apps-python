# Episode 13: Text Splitting
# Build AI Apps with Python in Neovim

# A longer company handbook for splitting
handbook = """
Acme Corp Employee Handbook - 2026 Edition

Chapter 1: Remote Work Policy
All employees may work remotely up to 3 days per week. Remote work requires manager approval via the WorkFlex portal. Employees must be available during core hours (10 AM to 4 PM) regardless of location. Fridays are mandatory in-office collaboration days. International remote work requires HR approval and may have tax implications.

Chapter 2: Leave Policy
Annual leave: 18 days per year for all full-time employees. Unused leave can be carried over up to 5 days into the next year. Sick leave: 14 days per year. No doctor note is needed for absences of 1-2 days. For 3 or more consecutive sick days, a medical certificate is required. Parental leave: 16 weeks fully paid for all new parents, regardless of gender. Adoption leave follows the same policy.

Chapter 3: Compensation and Benefits
Salary reviews happen annually in March. Performance bonuses are paid in April based on the previous year. All employees receive medical insurance covering dental and vision. The company matches retirement contributions up to 5 percent of base salary.

Chapter 4: Tech Allowance
Every employee receives $2,500 per year for equipment purchases. Claims are submitted through the TechGear portal within 30 days of purchase. Approved items include: laptops, monitors, keyboards, mice, headphones, and ergonomic chairs. Software subscriptions up to $500 per year are covered separately under the Tools budget.

Chapter 5: Professional Development
Each employee gets $1,500 per year for training and conferences. Courses must be relevant to your current role or planned career path. Time off for approved training counts as work hours. Managers must approve all training requests at least 2 weeks in advance.
"""

# Simple text splitter — by character count with overlap
def split_text(text, chunk_size=500, overlap=50):
  chunks = []
  start = 0
  while start < len(text):
    end = start + chunk_size
    chunk = text[start:end]
    chunks.append(chunk.strip())
    start = end - overlap
  return [c for c in chunks if c]

# Split and display
chunks = split_text(handbook, chunk_size=500, overlap=50)

print(f"Document length: {len(handbook)} characters")
print(f"Chunk size: 500, Overlap: 50")
print(f"Number of chunks: {len(chunks)}")
print("=" * 50)

for i, chunk in enumerate(chunks):
  print(f"\nChunk {i + 1} ({len(chunk)} chars):")
  print("-" * 40)
  print(chunk[:200] + "..." if len(chunk) > 200 else chunk)

# Try different settings
print("\n\n=== Different chunk sizes ===")
for size in [200, 500, 1000]:
  chunks = split_text(handbook, chunk_size=size, overlap=50)
  print(f"Size {size}: {len(chunks)} chunks")
