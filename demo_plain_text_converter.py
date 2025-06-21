#!/usr/bin/env python3
"""
Demo Script for Plain Text to Markdown Converter

This script demonstrates how to use the new PlainTextConverter feature
to convert various plain text files to markdown format.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.document_converter_manager import DocumentConverterManager
from services.plain_text_converter import PlainTextConverter


def create_demo_files():
    """Create demo files to showcase the converter capabilities."""
    demo_dir = Path("demo_files")
    demo_dir.mkdir(exist_ok=True)
    
    print(f"Creating demo files in: {demo_dir.absolute()}")
    
    # Demo CSV file
    csv_content = """Employee ID,Name,Department,Salary,Start Date
001,Alice Johnson,Engineering,75000,2023-01-15
002,Bob Smith,Marketing,65000,2023-02-01
003,Carol Davis,Engineering,80000,2022-11-10
004,David Wilson,Sales,70000,2023-03-05
005,Eva Brown,HR,60000,2022-12-20"""
    
    csv_file = demo_dir / "employees.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    print(f"✅ Created: {csv_file.name}")
    
    # Demo TSV file
    tsv_content = """Product	Category	Price	Stock	Supplier
Laptop	Electronics	999.99	25	TechCorp
Mouse	Electronics	29.99	150	TechCorp
Desk	Furniture	299.99	10	OfficePlus
Chair	Furniture	199.99	20	OfficePlus
Monitor	Electronics	249.99	30	TechCorp"""
    
    tsv_file = demo_dir / "inventory.tsv"
    with open(tsv_file, 'w', encoding='utf-8') as f:
        f.write(tsv_content)
    print(f"✅ Created: {tsv_file.name}")
    
    # Demo plain text file
    txt_content = """Project Status Report

Executive Summary
The Q1 development project is progressing well with most milestones on track. We have successfully completed the initial design phase and are now moving into implementation.

Key Achievements
- Completed user interface mockups
- Finalized database schema design
- Set up development environment
- Conducted initial security review

Current Challenges
Resource allocation has been tight due to competing priorities. The team is working overtime to maintain the schedule.

Timeline Update
Phase 1: Design (Completed)
Phase 2: Implementation (In Progress - 60% complete)
Phase 3: Testing (Scheduled for April)
Phase 4: Deployment (Scheduled for May)

Budget Status
Current spend: $45,000 of $75,000 budget
Remaining: $30,000
Projected final cost: $72,000

Risk Assessment
Low risk: Technical implementation
Medium risk: Resource availability
High risk: Third-party integration delays

Next Steps
1. Complete core functionality implementation
2. Begin integration testing
3. Prepare user acceptance testing plan
4. Schedule stakeholder review meeting

Contact Information
Project Manager: Sarah Chen (sarah.chen@company.com)
Technical Lead: Mike Rodriguez (mike.rodriguez@company.com)"""
    
    txt_file = demo_dir / "project_report.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    print(f"✅ Created: {txt_file.name}")
    
    # Demo log file
    log_content = """2024-01-15 09:00:00 INFO System startup initiated
2024-01-15 09:00:05 INFO Database connection established
2024-01-15 09:00:10 INFO User authentication service started
2024-01-15 09:15:23 INFO User login: alice@company.com
2024-01-15 09:30:45 WARN High CPU usage detected: 85%
2024-01-15 09:31:00 INFO CPU usage normalized: 45%
2024-01-15 10:00:00 INFO Hourly backup started
2024-01-15 10:05:30 INFO Hourly backup completed successfully
2024-01-15 10:15:12 ERROR Failed to process payment: timeout
2024-01-15 10:15:15 INFO Retrying payment processing
2024-01-15 10:15:18 INFO Payment processed successfully
2024-01-15 11:00:00 INFO System health check: All services operational
2024-01-15 12:00:00 INFO Daily report generation started
2024-01-15 12:03:45 INFO Daily report generation completed"""
    
    log_file = demo_dir / "system.log"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(log_content)
    print(f"✅ Created: {log_file.name}")
    
    return demo_dir


def demo_individual_converter():
    """Demonstrate using PlainTextConverter directly."""
    print("\n" + "="*60)
    print("DEMO: Using PlainTextConverter Directly")
    print("="*60)
    
    # Create converter
    converter = PlainTextConverter()
    
    # Show converter info
    info = converter.get_converter_info()
    print(f"Converter: {info['name']}")
    print(f"AI Enabled: {info['ai_enabled']}")
    if info['ai_enabled']:
        print(f"AI Service: {info['ai_service']} ({info['ai_model']})")
    print(f"Supported Extensions: {info['supported_extensions']}")
    
    # Convert a single file
    demo_dir = Path("demo_files")
    csv_file = demo_dir / "employees.csv"
    output_file = demo_dir / "employees_direct.md"
    
    if csv_file.exists():
        print(f"\nConverting: {csv_file.name}")
        success = converter.convert_file(csv_file, output_file)
        print(f"Success: {'✅ Yes' if success else '❌ No'}")
        
        if success and output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"Output preview:\n{content[:300]}...")


def demo_document_manager():
    """Demonstrate using DocumentConverterManager with plain text files."""
    print("\n" + "="*60)
    print("DEMO: Using DocumentConverterManager")
    print("="*60)
    
    # Create manager
    demo_dir = Path("demo_files")
    output_dir = demo_dir / "output"
    
    manager = DocumentConverterManager(
        input_folder=demo_dir,
        output_folder=output_dir
    )
    
    # Show available converters
    print("Available converters:")
    for converter in manager.converters:
        info = converter.get_converter_info()
        print(f"  - {info['name']}: {info['supported_extensions']}")
    
    # Convert all files
    print(f"\nConverting all files in: {demo_dir}")
    results = manager.convert_all()
    
    print(f"Results:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Successful: {results['successful_conversions']}")
    print(f"  Failed: {results['failed_conversions']}")
    
    # Show generated files
    if output_dir.exists():
        print(f"\nGenerated markdown files:")
        for md_file in output_dir.glob("*.md"):
            print(f"  📄 {md_file.name}")


def show_output_samples():
    """Show samples of the generated markdown files."""
    print("\n" + "="*60)
    print("DEMO: Generated Markdown Samples")
    print("="*60)
    
    output_dir = Path("demo_files/output")
    if not output_dir.exists():
        print("No output directory found. Run the conversion demo first.")
        return
    
    for md_file in output_dir.glob("*.md"):
        print(f"\n📄 {md_file.name}")
        print("-" * 40)
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Show first 500 characters
        preview = content[:500]
        if len(content) > 500:
            preview += "..."
        
        print(preview)


def main():
    """Main demo function."""
    print("Plain Text to Markdown Converter Demo")
    print("="*60)
    
    try:
        # Create demo files
        demo_dir = create_demo_files()
        
        # Demo individual converter
        demo_individual_converter()
        
        # Demo document manager
        demo_document_manager()
        
        # Show output samples
        show_output_samples()
        
        print("\n" + "="*60)
        print("DEMO SUMMARY")
        print("="*60)
        print("✅ Demo completed successfully!")
        print(f"📁 Demo files are in: {demo_dir.absolute()}")
        print(f"📁 Output files are in: {demo_dir.absolute()}/output")
        print("\nFeatures demonstrated:")
        print("  ✅ CSV to markdown table conversion")
        print("  ✅ TSV to markdown table conversion")
        print("  ✅ Plain text to structured markdown")
        print("  ✅ Log file to organized markdown")
        print("  ✅ AI-enhanced text analysis (when available)")
        print("  ✅ Integration with DocumentConverterManager")
        
        print("\nYou can now:")
        print("  1. Examine the generated markdown files")
        print("  2. Place your own text files in the demo_files directory")
        print("  3. Run the DocumentConverterManager to convert them")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
