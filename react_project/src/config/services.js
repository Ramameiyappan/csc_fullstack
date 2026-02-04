export const services = [
  {
    name: "Electricity",
    endpoint: "/category/electricity/",
    fields: [
      { name: "customer_name", label: "Customer Name" },
      { name: "account_no", label: "EB Account Number", type: "number" },
      { name: "amount", label: "Amount", type: "decimal", step: "0.01" },
      { name: "commission", label: "Commission", type: "decimal", step: "0.01" },
      { name: "iscsc", label: "Is CSC Transaction?", type: "checkbox"}
    ],
  },
  {
    name: "Recharge",
    endpoint: "/category/recharge/",
    fields: [
      { name: "customer_name", label: "Mobile Brand", type: "select", options: ['airtel', 'bsnl', 'jio', 'vi'] },
      { name: "mobile", label: "Mobile Number", type: "number" },
      { name: "amount", label: "Amount", type: "decimal", step: "0.01" },
      { name: "commission", label: "Commission", type: "decimal", step: "0.01" },
      { name: "iscsc", label: "Is CSC Transaction?", type: "checkbox"}
    ],
  },
  {
    name: "PAN",
    endpoint: "/category/pan/",
    fields: [
      { name: "customer_name", label: "Applicant Name" },
      { name: "mobile", label: "Mobile Number", type: "number" },
      { name: "account_no", label: "Service Provided", type: "select", options: ['uti', 'nsdl']  },
      { name: "iscsc", label: "Is CSC Transaction?", type: "checkbox"}
    ],
  },
  {
    name: "Topup",
    endpoint: "/category/topup/",
    fields: [{ name: "topup", label: "Topup Amount", type: "decimal", step: "0.01" }],
  },
  {
    name: "Travel",
    endpoint: "/category/travel/",
    fields: [
      { name: "work_name", label: "Travel Type", type: "select", options: ['train', 'bus', 'flight'] },
      { name: "customer_name", label: "Customer Name" },
      { name: "account_no", label: "Travel PNR Number"},
      { name: "mobile", label: "Mobile Number", type: "number" },
      { name: "amount", label: "Amount", type: "decimal", step: "0.01" },
      { name: "commission", label: "Commission", type: "decimal", step: "0.01" },
      { name: "iscsc", label: "Is CSC Transaction?", type: "checkbox"}
    ],
  },
  {
    name: "Insurance",
    endpoint: "/category/insurance/",
    fields: [
      { name: "work_name", label: "Insurance For", type: "select", options: ['car', 'bike', 'health', 'crop'] },
      { name: "customer_name", label: "Customer Name" },
      { name: "account_no", label: "Policy Number"},
      { name: "mobile", label: "Mobile Number", type: "number" },
      { name: "amount", label: "Amount", type: "decimal", step: "0.01" },
      { name: "commission", label: "Commission", type: "decimal", step: "0.01" },
      { name: "iscsc", label: "Is CSC Transaction?", type: "checkbox"}
    ],
  },
  {
    name: "E-Sevai",
    endpoint: "/category/esevai/",
    fields: [
      { name: "customer_name", label: "Customer Name" },
      { name: "account_no", label: "Certificate Number"},
      { name: "mobile", label: "Mobile Number", type: "number" },
      { name: "amount", label: "Amount", type: "decimal", step: "0.01" },
      { name: "commission", label: "Commission", type: "decimal", step: "0.01" },
      { name: "iscsc", label: "Is CSC Transaction?", type: "checkbox"}
    ],
  },
  {
    name: "Online Service",
    endpoint: "/category/online/",
    fields: [
      { name: "customer_name", label: "Customer Name" },
      { name: "account_no", label: "Application Number"},
      { name: "mobile", label: "Mobile Number", type: "number" },
      { name: "amount", label: "Amount", type: "decimal", step: "0.01" },
      { name: "commission", label: "Commission", type: "decimal", step: "0.01" },
      { name: "iscsc", label: "Is CSC Transaction?", type: "checkbox"}
    ],
  },
];
