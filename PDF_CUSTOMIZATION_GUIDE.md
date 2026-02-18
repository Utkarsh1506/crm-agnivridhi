# PDF Template Customization Guide

## How to Add Your Sample Agreement PDFs

Aapne kaha tha ki aap sample agreement PDFs provide karoge. Yahan bataya gaya hai ki unhe kaise integrate karein.

## Option 1: PDF ko HTML mein Convert Karo (Recommended)

### Funding Agreement:
1. Apna funding agreement PDF kholo
2. Uski content ko HTML format mein convert karo
3. `templates/agreements/pdf/funding_agreement.html` file edit karo
4. Apni content paste karo

### Website Agreement:
Same process `templates/agreements/pdf/website_agreement.html` ke liye

## Option 2: Existing Template Customize Karo

Maine already basic templates create kar diye hain. Inhe customize kar sakte ho:

### Variable Fields (These will be auto-filled):

```django
{{ agreement.service_receiver_name }}          - Service Receiver ka naam
{{ agreement.service_receiver_address }}       - Address
{{ agreement.date_of_agreement }}              - Agreement date
{{ agreement.service_description }}            - Service description
{{ agreement.total_amount_pitched }}           - Total amount
{{ agreement.received_amount_stage1 }}         - Received amount Stage 1
{{ agreement.pending_amount_stage2 }}          - Pending amount Stage 2
{{ agreement.commission_percentage }}          - Commission %
{{ agreement.get_commission_stage_display }}   - Commission stage name
{{ agreement.calculated_commission }}          - Auto-calculated commission amount
{{ agreement.agreement_number }}               - Auto-generated agreement number
{{ today }}                                    - Current date
```

### Conditional Display (for Pending Amount):

```django
{% if agreement.has_pending_amount %}
    <!-- Show pending amount row -->
    <tr>
        <td>Pending Amount (Stage 2)</td>
        <td>₹{{ agreement.pending_amount_stage2|floatformat:2 }}</td>
    </tr>
{% endif %}
```

## Template Structure

### Header Section
```html
<div class="header">
    <h1>YOUR COMPANY NAME</h1>
    <p>YOUR COMPANY TAGLINE</p>
    <p>Contact: +91-XXXXXXXXXX | Email: your@email.com</p>
</div>
```

### Agreement Number
```html
<div class="agreement-number">
    Agreement No: {{ agreement.agreement_number }}
</div>
```

### Service Receiver Details
```html
<div class="section">
    <div class="section-title">SERVICE RECEIVER DETAILS</div>
    <div class="field">
        <span class="field-label">Name:</span>
        <span class="field-value">{{ agreement.service_receiver_name }}</span>
    </div>
    <div class="field">
        <span class="field-label">Address:</span>
        <span class="field-value">{{ agreement.service_receiver_address|linebreaks }}</span>
    </div>
</div>
```

### Financial Table
```html
<table class="financial-table">
    <tr>
        <th>Particulars</th>
        <th style="text-align: right;">Amount (INR)</th>
    </tr>
    <tr>
        <td>Total Amount Pitched</td>
        <td style="text-align: right;">₹ {{ agreement.total_amount_pitched|floatformat:2 }}</td>
    </tr>
    <!-- Add more rows as needed -->
</table>
```

### Terms and Conditions
```html
<div class="section terms">
    <div class="section-title">TERMS AND CONDITIONS</div>
    
    <p><strong>1. Your Term Title:</strong> Your term description...</p>
    
    <p><strong>2. Payment Terms:</strong></p>
    <ul>
        <li>Stage 1 payment of ₹{{ agreement.received_amount_stage1|floatformat:2 }}</li>
        {% if agreement.has_pending_amount %}
        <li>Stage 2 payment of ₹{{ agreement.pending_amount_stage2|floatformat:2 }}</li>
        {% endif %}
    </ul>
</div>
```

### Signatures Section
```html
<div class="signature-section">
    <div class="signature-box" style="float: left;">
        <div class="signature-line">
            <strong>Service Receiver Signature</strong><br>
            Name: {{ agreement.service_receiver_name }}<br>
            Date: ________________
        </div>
    </div>
    <div class="signature-box" style="float: right;">
        <div class="signature-line">
            <strong>YOUR COMPANY NAME</strong><br>
            Authorized Signatory<br>
            Date: {{ today|date:"d F, Y" }}
        </div>
    </div>
</div>
```

## Styling Customization

Templates mein `<style>` tag hai jahan CSS hai. Customize kar sakte ho:

### Colors
```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
}
```

### Fonts
```css
body {
    font-family: 'Arial', sans-serif;
    font-size: 11pt;
    line-height: 1.6;
}
```

### Page Setup
```css
@page {
    size: A4;
    margin: 2cm;
}
```

## Example: Adding Your Logo

```html
<!-- In header section -->
<div class="header" style="text-align: center;">
    <img src="{% static 'images/company-logo.png' %}" alt="Company Logo" style="height: 60px;">
    <h1>YOUR COMPANY NAME</h1>
</div>
```

Note: Logo file ko `static/images/` folder mein rakhna hoga.

## Differences Between Funding & Website Templates

### Funding Agreement Should Have:
- Loan amount details
- Disbursement terms
- Commission after loan sanctioning
- Bank/NBFC related terms

### Website Agreement Should Have:
- Project scope
- Deliverables list
- Revision policy
- Hosting/domain details
- Intellectual property clause

## Testing Your Templates

1. Agreement create karo test data se
2. PDF download karo
3. Check karo:
   - All variable fields filled hain?
   - Formatting sahi hai?
   - Page breaks proper hain?
   - Signatures section sahi jagah hai?

## Common Issues & Solutions

### Issue: PDF mein Hindi text properly display nahi ho raha
**Solution**: Font specify karo jo Hindi support karta hai:
```css
body {
    font-family: 'Noto Sans Devanagari', Arial, sans-serif;
}
```

### Issue: Page breaks wrong jagah aa rahe hain
**Solution**: Use `page-break-inside: avoid`:
```css
.signature-section {
    page-break-inside: avoid;
}
```

### Issue: Images display nahi ho rahe
**Solution**: 
- Verify image path
- Use absolute paths in production
- Check MEDIA_URL settings

## Sample Agreement Content

### Funding Agreement - Key Clauses:

1. **Loan Facilitation**: Company will facilitate loan from bank/NBFC
2. **Fee Structure**: 
   - Stage 1: Processing fee (before loan sanction)
   - Stage 2: Service fee (after disbursement)
   - Commission: X% on disbursed amount
3. **Documents Required**: List of documents
4. **Timeline**: Expected processing time
5. **Refund Policy**: If loan is not approved
6. **Liability Clause**: Company's responsibilities and limitations

### Website Agreement - Key Clauses:

1. **Project Scope**: Detailed list of deliverables
2. **Payment Terms**:
   - Advance: X% at start
   - Milestone payments
   - Final payment after delivery
3. **Timeline**: Development phases with dates
4. **Revisions**: Number of revision rounds included
5. **Content**: Who provides content (client/company)
6. **Hosting & Domain**: Responsibility and costs
7. **Maintenance**: Post-launch support period
8. **IP Rights**: Ownership after full payment
9. **Confidentiality**: NDA clause
10. **Termination**: Conditions for contract termination

## Pro Tips

1. **Keep It Legal**: Consult with legal advisor for proper terms
2. **Clear Language**: Use simple, understandable language
3. **Numbered Clauses**: Easy to reference specific points
4. **Bold Important**: Bold key terms and amounts
5. **White Space**: Don't overcrowd the page
6. **Print Preview**: Test print before finalizing
7. **Version Control**: Keep older versions backed up

## File Locations

**Templates to Edit:**
```
templates/agreements/pdf/
├── funding_agreement.html    ← Edit this for funding agreements
└── website_agreement.html    ← Edit this for website agreements
```

**To Add Company Logo:**
```
static/images/
└── company-logo.png          ← Add your logo here
```

## Need Help?

Agar kuch samajh nahi aa raha toh:
1. Existing template ko carefully dekho
2. Variable names ko preserve rakho
3. Django template tags ({% %} and {{ }}) ko mat hatao
4. Test karte raho local environment pe

---

**Remember**: 
- Template variables ko change mat karna: {{ agreement.field_name }}
- Django tags preserve rakho: {% if %}, {% for %}, etc.
- Styling freely customize kar sakte ho
- Terms and conditions apne according change karo

Aap jab apne sample PDFs doge, main unhe HTML mein convert karne mein help kar sakta hoon! 🚀
