#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Search - BM25 search engine for UI/UX style guides
Usage: python search.py "<query>" [--domain <domain>] [--stack <stack>] [--max-results 3]
       python search.py "<query>" --design-system [-p "Project Name"]
       python search.py "<query>" --design-system --persist [-p "Project Name"] [--page "dashboard"]

Domains: style, prompt, color, chart, landing, product, ux, typography
Stacks: html-tailwind, react, nextjs

Persistence (Master + Overrides pattern):
  --persist    Save design system to design-system/MASTER.md
  --page       Also create a page-specific override file in design-system/pages/
"""

import argparse
import sys
import io
from core import CSV_CONFIG, AVAILABLE_STACKS, MAX_RESULTS, search, search_stack, audit_page
from design_system import generate_design_system, persist_design_system

# Force UTF-8 for stdout/stderr to handle emojis on Windows (cp1252 default)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def format_output(result):
    """Format results for Claude consumption (token-optimized)"""
    if "error" in result:
        return f"Error: {result['error']}"

    output = []
    if result.get("stack"):
        output.append(f"## UI Pro Max Stack Guidelines")
        output.append(f"**Stack:** {result['stack']} | **Query:** {result['query']}")
    else:
        output.append(f"## UI Pro Max Search Results")
        output.append(f"**Domain:** {result['domain']} | **Query:** {result['query']}")
    output.append(f"**Source:** {result['file']} | **Found:** {result['count']} results\n")

    for i, row in enumerate(result['results'], 1):
        output.append(f"### Result {i}")
        for key, value in row.items():
            value_str = str(value)
            if len(value_str) > 300:
                value_str = value_str[:300] + "..."
            output.append(f"- **{key}:** {value_str}")
        output.append("")

    return "\n".join(output)


def format_audit_output(result):
    """Format audit results as a comprehensive checklist"""
    output = []
    page_type = result["page_type"]
    standard = result["standard"]
    seo = result["seo"]
    rules = result["rules"]

    output.append("=" * 60)
    output.append(f"  PAGE AUDIT: {page_type.title()}")
    output.append("=" * 60)

    if standard:
        output.append("")
        output.append("REQUIRED SECTIONS:")
        for section in standard.get("Required Sections", "").split(", "):
            if section.strip():
                output.append(f"  [ ] {section.strip()}")

        output.append("")
        output.append("RECOMMENDED SECTIONS:")
        for section in standard.get("Recommended Sections", "").split(", "):
            if section.strip():
                output.append(f"  [ ] {section.strip()}")

        output.append("")
        output.append("NAV REQUIREMENTS:")
        for req in standard.get("Nav Requirements", "").split(", "):
            if req.strip():
                output.append(f"  [ ] {req.strip()}")

        output.append("")
        output.append("FOOTER REQUIREMENTS:")
        for req in standard.get("Footer Requirements", "").split(", "):
            if req.strip():
                output.append(f"  [ ] {req.strip()}")

        output.append("")
        output.append("INTERNAL LINKS:")
        for link in standard.get("Internal Links", "").split(", "):
            if link.strip():
                output.append(f"  [ ] {link.strip()}")

        output.append("")
        output.append("COMMON VIOLATIONS TO CHECK:")
        for violation in standard.get("Common Violations", "").split(", "):
            if violation.strip():
                output.append(f"  [!] {violation.strip()}")
    else:
        output.append(f"\n  No standard found for page type: {page_type}")
        output.append("  Available types: Landing, Sign Up, Sign In, Dashboard, Pricing, Blog List, Blog Post, PDP, Search Results, Checkout, 404, Contact, About, Settings")

    if seo:
        output.append("")
        output.append("-" * 40)
        output.append("SEO REQUIREMENTS:")
        output.append(f"  Title Format:  {seo.get('Title Format', 'N/A')}")
        output.append(f"  Meta Desc:     {seo.get('Meta Description', 'N/A')[:80]}...")
        output.append(f"  Schema:        {seo.get('Schema Type', 'N/A')}")
        output.append(f"  Indexing:      {seo.get('Indexing', 'N/A')}")
        output.append(f"  Canonical:     {seo.get('Canonical', 'N/A')}")
        output.append(f"  Open Graph:    {seo.get('Open Graph', 'N/A')[:80]}...")
        output.append(f"  Headings:      {seo.get('Heading Structure', 'N/A')[:80]}...")

    if rules:
        output.append("")
        output.append("-" * 40)
        output.append(f"AUDIT RULES ({len(rules)} checks):")
        for rule in rules:
            severity = rule.get("Severity", "MEDIUM")
            severity_tag = {"CRITICAL": "[!!]", "HIGH": "[! ]", "MEDIUM": "[  ]", "LOW": "[  ]"}.get(severity, "[  ]")
            output.append(f"  {severity_tag} {rule.get('Rule ID', '?')}: {rule.get('Rule Description', '')}")
            output.append(f"       Fix: {rule.get('Fix Suggestion', '')[:100]}")

    output.append("")
    output.append("=" * 60)
    output.append(f"Total checks: {result['total_checks']} rules")
    critical_count = sum(1 for r in rules if r.get("Severity") == "CRITICAL")
    high_count = sum(1 for r in rules if r.get("Severity") == "HIGH")
    if critical_count or high_count:
        output.append(f"  CRITICAL: {critical_count} | HIGH: {high_count}")
    output.append("=" * 60)

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI Pro Max Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Search domain")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="Stack-specific search (html-tailwind, react, nextjs)")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max results (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    # Design system generation
    parser.add_argument("--design-system", "-ds", action="store_true", help="Generate complete design system recommendation")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name for design system output")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Output format for design system")
    # Persistence (Master + Overrides pattern)
    parser.add_argument("--persist", action="store_true", help="Save design system to design-system/MASTER.md (creates hierarchical structure)")
    parser.add_argument("--page", type=str, default=None, help="Create page-specific override file in design-system/pages/")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Output directory for persisted files (default: current directory)")
    # Page audit
    parser.add_argument("--audit", "-a", type=str, default=None, help="Audit a page type against standards. E.g., --audit landing")

    args = parser.parse_args()

    # Audit takes highest priority
    if args.audit:
        result = audit_page(args.audit)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        else:
            print(format_audit_output(result))
    # Design system takes priority
    elif args.design_system:
        result = generate_design_system(
            args.query, 
            args.project_name, 
            args.format,
            persist=args.persist,
            page=args.page,
            output_dir=args.output_dir
        )
        print(result)
        
        # Print persistence confirmation
        if args.persist:
            project_slug = args.project_name.lower().replace(' ', '-') if args.project_name else "default"
            print("\n" + "=" * 60)
            print(f"✅ Design system persisted to design-system/{project_slug}/")
            print(f"   📄 design-system/{project_slug}/MASTER.md (Global Source of Truth)")
            if args.page:
                page_filename = args.page.lower().replace(' ', '-')
                print(f"   📄 design-system/{project_slug}/pages/{page_filename}.md (Page Overrides)")
            print("")
            print(f"📖 Usage: When building a page, check design-system/{project_slug}/pages/[page].md first.")
            print(f"   If exists, its rules override MASTER.md. Otherwise, use MASTER.md.")
            print("=" * 60)
    # Stack search
    elif args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
    # Domain search
    else:
        result = search(args.query, args.domain, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
