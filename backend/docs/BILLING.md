# 🧾 **CortexLayer Billing System — Source of Truth**

This document defines **all billing, usage tracking, cost accounting, and subscription rules** for the CortexLayer Support Agent backend.

Everything related to money, limits, tokens, and cost must match this specification.

---

# **1. Plan Tiers**

| Plan        | Price   | Query Limit | Max Docs | Max File Size | Chunks/Doc | Rate Limit | WhatsApp | Model Priority                 |
| ----------- | ------- | ----------- | -------- | ------------- | ---------- | ---------- | -------- | ------------------------------ |
| **Starter** | $79/mo  | 1,000/mo    | 10       | 5MB           | 250        | 15/min     | ❌        | Mixtral-8x7B                   |
| **Growth**  | $199/mo | 5,000/mo    | 50       | 10MB          | 500        | 50/min     | 2,000    | Mixtral + GPT-4o-mini fallback |
| **Scale**   | $349/mo | 50,000/mo   | 1000     | 20MB          | 3000       | 100/min    | 10,000   | GPT-4o primary                 |

Plans determine:

* Allowed number of queries
* Allowed number of documents
* File upload size
* Max chunk count
* Rate limiting
* Whether WhatsApp automation is enabled
* Whether fallback models can be used

---

# **2. Usage Tracking — UsageLog Ledger**

Every billable operation creates a row in `usage_logs`.

This is the **financial ledger** of CortexLayer.

### Fields:

| Field              | Meaning                                       |
| ------------------ | --------------------------------------------- |
| `client_id`        | whose usage this belongs to                   |
| `operation_type`   | `"query"` / `"embedding"` / `"whatsapp"`      |
| `input_tokens`     | prompt tokens                                 |
| `output_tokens`    | LLM output tokens                             |
| `embedding_tokens` | tokens sent to embedding model                |
| `cost_usd`         | final billed cost snapshot                    |
| `model_used`       | which model was used                          |
| `latency_ms`       | execution latency                             |
| `extra`            | JSON metadata (document_id, chunk_index, etc) |
| `timestamp`        | when the event happened                       |

---

# **3. Internal Provider Pricing (Used for Cost Calculation)**

The backend contains this structure:

```python
PRICING = {
    "text-embedding-3-small": {"input": 0.02},
    "mixtral-8x7b": {"input": 0.27, "output": 0.27},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "whatsapp_message": 0.005,
}
```

### ❗ IMPORTANT DISTINCTION

### **PRICING = CortexLayer’s internal costs**

Not customer prices.
Not plan prices.
Not per-token charges to users.

This dictionary is only for:

* estimating CortexLayer's real expenses
* calculating overage billing (query overuse)
* usage analytics
* profitability measurements

### Customers do **NOT** pay per-token bills.

They pay based on **plans + overage** only.

### Groq free limits do NOT affect pricing

We **do not pass through** provider freebies to end users, to avoid unstable pricing.

---

# **4. Billing Flow Examples**

## **4.1 Document Upload → Embedding**

Uploading a PDF:

1. PDF processed
2. Chunked
3. Each chunk embedded
4. Each embedding creates a usage log row:

```
operation_type="embedding"
embedding_tokens=1530
model_used="text-embedding-3-small"
cost_usd = calculate_embedding_cost()
extra={"document_id": "...", "chunk_index": 7}
```

---

## **4.2 User Query (Widget / API)**

```
operation_type="query"
input_tokens=120
output_tokens=480
model_used="mixtral-8x7b"
cost_usd = calculate_generation_cost()
extra={"query_id": "..."}
```

---

## **4.3 WhatsApp Message**

Two rows:

### Inbound message fee:

```
operation_type="whatsapp"
cost_usd=0.005
extra={"direction": "inbound"}
```

### LLM response:

```
operation_type="query"
input_tokens=80
output_tokens=145
model_used="gpt-4o-mini"
```

---

# **5. Plan Limits & Enforcement**

Each plan defines:

* Max queries per month
* Max documents
* Max chunk count per document
* Max file upload size
* WhatsApp allocations
* Query rate limits

If limits are exceeded → *overage logic triggers*.

---

# **6. Overage Billing**

Each plan allows:

* **Soft cap** = plan limit × 1.2
* **Hard cap** = plan limit × 1.5

Example (Starter):

* Limit: **1000**
* Soft cap: **1200**
* Hard cap: **1500**

### **Soft Cap → Overage Invoice**

```
overage_queries = used - plan_limit
overage_cost = overage_queries * $0.01
```

We create a Stripe invoice item.

### **Hard Cap → Disable**

* Disable the client
* Prevent new queries
* Set billing_status = `"DISABLED"`

---

# **7. Billing State Machine**

```
ACTIVE --(payment failed)--> GRACE_PERIOD
GRACE_PERIOD --(7 days)--> DISABLED
DISABLED --(manual admin action)--> ACTIVE
ACTIVE --(subscription cancelled)--> CANCELLED
```

Stripe events:

| Stripe Event                    | Behavior               |
| ------------------------------- | ---------------------- |
| `invoice.paid`                  | account becomes ACTIVE |
| `invoice.payment_failed`        | enters GRACE_PERIOD    |
| `customer.subscription.deleted` | becomes CANCELLED      |

---

# **8. Stripe Integration Responsibilities**

Stripe does:

* Customer creation
* Subscription lifecycle
* Automatic billing
* Payment retries
* Webhooks
* Invoices

CortexLayer does:

* Logging usage
* Calculating cost
* Enforcing limits
* Generating overage invoice items
* Updating client billing status

---

# **9. Required Database Tables**

### **Client**

* plan_type
* billing_status
* stripe_customer_id
* is_disabled

### **UsageLog**

* full ledger of all operations

### **Document**

* used for enforcing upload limits

---

# **10. Summary**

The CortexLayer billing engine ensures:

* Predictable customer billing (plan-based)
* Accurate overage billing
* Full internal cost tracking
* Auditable usage logs
* Automatic disabling on abuse
* Stripe-backed reliability
* Support for WhatsApp usage
* Clear financial analytics

This document is the **authoritative blueprint** for billing across the platform.