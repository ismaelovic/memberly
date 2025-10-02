import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getEnv } from "../utils/envUtils";
import styles from "../modules/OnboardTenant.module.css";
import CreatableSelect from "react-select/creatable";

const createOption = (label) => ({
  label,
  value: label,
});

const OnboardTenant = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    user: {
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      confirmPassword: "",
      dateOfBirth: "",
      address: "",
      zipCode: "",
    },
    tenant: {
      tenantName: "",
      tenantAddress: "",
      tenantPhone: "",
    },
    subscriptions: [],
  });
  const [errors, setErrors] = useState({});
  const [visitedSteps, setVisitedSteps] = useState(new Set([1]));

  const steps = [
    { number: 1, title: "Welcome", icon: "👋" },
    { number: 2, title: "User Information", icon: "👤" },
    { number: 3, title: "Tenant Information", icon: "🏢" },
    { number: 4, title: "Subscription Plans", icon: "💳" },
    { number: 5, title: "Password Setup", icon: "🔒" },
    { number: 6, title: "Confirmation", icon: "✅" },
    { number: 7, title: "Payment Details", icon: "💳" },
  ];

  const updateFormData = (section, field, value) => {
    setFormData((prev) => {
      if (field === null) {
        // Handle array updates (e.g., subscriptions)
        return {
          ...prev,
          [section]: value,
        };
      }

      return {
        ...prev,
        [section]: {
          ...prev[section],
          [field]: value,
        },
      };
    });

    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: "" }));
    }
  };

  const validateStep = (step) => {
    const newErrors = {};

    switch (step) {
      case 1:
        if (!formData.user.firstName.trim())
          newErrors.firstName = "First name is required";
        if (!formData.user.lastName.trim())
          newErrors.lastName = "Last name is required";
        if (!formData.user.email.trim()) newErrors.email = "Email is required";
        if (!formData.user.password)
          newErrors.password = "Password is required";
        if (formData.user.password !== formData.user.confirmPassword) {
          newErrors.confirmPassword = "Passwords do not match";
        }
        if (!formData.user.dateOfBirth)
          newErrors.dateOfBirth = "Date of birth is required";
        if (!formData.user.address.trim())
          newErrors.address = "Address is required";
        if (!formData.user.zipCode.trim())
          newErrors.zipCode = "Zip code is required";
        break;
      case 2:
        if (!formData.tenant.tenantName.trim())
          newErrors.tenantName = "Tenant name is required";
        if (!formData.tenant.tenantAddress.trim())
          newErrors.tenantAddress = "Tenant address is required";
        if (!formData.tenant.tenantPhone.trim())
          newErrors.tenantPhone = "Tenant phone is required";
        break;
      case 3:
        if (formData.subscriptions.length === 0)
          newErrors.subscriptions =
            "At least one subscription plan is required";
        break;
      default:
        break;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const goToStep = (stepNumber) => {
    if (
      visitedSteps.has(stepNumber) ||
      stepNumber === Math.max(...visitedSteps) + 1
    ) {
      setCurrentStep(stepNumber);
      setVisitedSteps((prev) => new Set([...prev, stepNumber]));
    }
  };

  const nextStep = () => {
    // if (validateStep(currentStep)) {
    const newStep = currentStep + 1;
    setCurrentStep(newStep);
    setVisitedSteps((prev) => new Set([...prev, newStep]));
    // }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    if (!validateStep(4)) return;

    try {
      console.log("Form Data:", formData);

      // Ensure the formData is serialized correctly
      const payload = {
        user: {
          firstName: formData.user.firstName,
          lastName: formData.user.lastName,
          email: formData.user.email,
          password: formData.user.password,
          confirmPassword: formData.user.confirmPassword,
          dateOfBirth: formData.user.dateOfBirth,
          address: formData.user.address,
          zipCode: formData.user.zipCode,
        },
        tenant: {
          tenantName: formData.tenant.tenantName,
          tenantAddress: formData.tenant.tenantAddress,
          tenantPhone: formData.tenant.tenantPhone,
        },
        subscriptions: formData.subscriptions.map((sub) => ({
          name: sub.name,
          price: sub.price,
          features: sub.features,
        })),
      };

      const response = await fetch(
        `${getEnv("VITE_API_URL")}/api/onboarding/complete`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        throw new Error("Onboarding failed");
      }

      const { checkoutUrl } = await response.json();
      window.location.href = checkoutUrl;
    } catch (error) {
      setErrors({ submit: error.message });
    }
  };

  const renderProgressBar = () => (
    <div className={styles.progressContainer}>
      <div className={styles.progressBar}>
        {steps.map((step, index) => {
          const isActive = currentStep === step.number;
          const isCompleted = currentStep > step.number;
          const isVisited = visitedSteps.has(step.number);
          const isClickable =
            isVisited || step.number === Math.max(...visitedSteps) + 1;

          return (
            <div key={step.number} className={styles.progressItem}>
              <div
                className={`${styles.progressStep} ${
                  isCompleted
                    ? styles.completed
                    : isActive
                    ? styles.active
                    : isVisited
                    ? styles.visited
                    : styles.inactive
                } ${isClickable ? styles.clickable : ""}`}
                onClick={() => isClickable && goToStep(step.number)}
              >
                <span className={styles.stepIcon}>{step.icon}</span>
                <span className={styles.stepNumber}>{step.number}</span>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={`${styles.progressLine} ${
                    isCompleted ? styles.completed : ""
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>
      <div className={styles.stepInfo}>
        <h2 className={styles.stepTitle}>{steps[currentStep - 1]?.title}</h2>
        <p className={styles.stepCounter}>
          Step {currentStep} of {steps.length}
        </p>
      </div>
    </div>
  );

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className={styles.stepContent}>
            <h3>Welcome to the Onboarding Process</h3>
            <p>
              Thank you for choosing our platform! This onboarding process will
              guide you through setting up your account, tenant information, and
              subscription plans. Let's get started!
            </p>
            <button
              onClick={nextStep}
              className={`${styles.navButton} ${styles.nextButton}`}
            >
              Start Onboarding →
            </button>
          </div>
        );
      case 2:
        return (
          <div className={styles.stepContent}>
            <h3>User Information</h3>
            <label>
              First Name:
              <input
                type="text"
                value={formData.user.firstName}
                onChange={(e) =>
                  updateFormData("user", "firstName", e.target.value)
                }
              />
            </label>
            <label>
              Last Name:
              <input
                type="text"
                value={formData.user.lastName}
                onChange={(e) =>
                  updateFormData("user", "lastName", e.target.value)
                }
              />
            </label>
            <label>
              Email:
              <input
                type="email"
                value={formData.user.email}
                onChange={(e) =>
                  updateFormData("user", "email", e.target.value)
                }
              />
            </label>
            <label>
              Date of Birth:
              <input
                type="date"
                value={formData.user.dateOfBirth}
                onChange={(e) =>
                  updateFormData("user", "dateOfBirth", e.target.value)
                }
                className={`${styles.input} ${
                  errors.dateOfBirth ? styles.inputError : ""
                }`}
              />
            </label>
            <label>
              Address:
              <input
                type="text"
                value={formData.user.address}
                onChange={(e) =>
                  updateFormData("user", "address", e.target.value)
                }
                className={`${styles.input} ${
                  errors.address ? styles.inputError : ""
                }`}
              />
            </label>
            <label>
              Zip Code:
              <input
                type="text"
                value={formData.user.zipCode}
                onChange={(e) =>
                  updateFormData("user", "zipCode", e.target.value)
                }
                className={`${styles.input} ${
                  errors.zipCode ? styles.inputError : ""
                }`}
              />
            </label>
          </div>
        );
      case 3:
        return (
          <div className={styles.stepContent}>
            <h3>Company Information</h3>
            <label>
              Name:
              <input
                type="text"
                value={formData.tenant.tenantName}
                onChange={(e) =>
                  updateFormData("tenant", "tenantName", e.target.value)
                }
              />
            </label>
            <label>
              Address:
              <input
                type="text"
                value={formData.tenant.tenantAddress}
                onChange={(e) =>
                  updateFormData("tenant", "tenantAddress", e.target.value)
                }
              />
            </label>
            <label>
              Corporate Phone:
              <input
                type="text"
                value={formData.tenant.tenantPhone}
                onChange={(e) =>
                  updateFormData("tenant", "tenantPhone", e.target.value)
                }
              />
            </label>
          </div>
        );
      case 4:
        return (
          <div className={styles.stepContent}>
            <h3>Define Subscription Plans</h3>
            <button
              onClick={() =>
                updateFormData("subscriptions", null, [
                  ...formData.subscriptions,
                  { name: "", price: 0, features: [] },
                ])
              }
            >
              Add Subscription Plan
            </button>
            {formData.subscriptions.map((plan, index) => (
              <div key={index}>
                <label>
                  Plan Name:
                  <input
                    type="text"
                    value={plan.name}
                    onChange={(e) => {
                      const updatedPlans = [...formData.subscriptions];
                      updatedPlans[index].name = e.target.value;
                      updateFormData("subscriptions", null, updatedPlans);
                    }}
                  />
                </label>
                <label>
                  Price:
                  <input
                    type="number"
                    value={plan.price}
                    onChange={(e) => {
                      const updatedPlans = [...formData.subscriptions];
                      updatedPlans[index].price =
                        parseFloat(e.target.value) || 0;
                      updateFormData("subscriptions", null, updatedPlans);
                    }}
                  />
                </label>
                <label>
                  Features:
                  <CreatableSelect
                    isMulti
                    value={plan.features.map((feature) =>
                      createOption(feature)
                    )}
                    onChange={(newValue) => {
                      const updatedPlans = [...formData.subscriptions];
                      updatedPlans[index].features = newValue.map(
                        (option) => option.value
                      );
                      updateFormData("subscriptions", null, updatedPlans);
                    }}
                    placeholder="Type a feature and press enter..."
                  />
                </label>
              </div>
            ))}
          </div>
        );
      case 5:
        return (
          <div className={styles.stepContent}>
            <h3>Password Setup</h3>
            <label>
              Password:
              <input
                type="password"
                value={formData.user.password}
                onChange={(e) =>
                  updateFormData("user", "password", e.target.value)
                }
              />
            </label>
            <label>
              Confirm Password:
              <input
                type="password"
                value={formData.user.confirmPassword}
                onChange={(e) =>
                  updateFormData("user", "confirmPassword", e.target.value)
                }
              />
            </label>
          </div>
        );
      case 6:
        return (
          <div className={styles.stepContent}>
            <h3>Confirmation</h3>
            <p>Review your details before submission:</p>

            <div className={styles.reviewSection}>
              <h4>User Information</h4>
              <p>
                <strong>First Name:</strong> {formData.user.firstName}
              </p>
              <p>
                <strong>Last Name:</strong> {formData.user.lastName}
              </p>
              <p>
                <strong>Email:</strong> {formData.user.email}
              </p>
              <p>
                <strong>Date of Birth:</strong> {formData.user.dateOfBirth}
              </p>
              <p>
                <strong>Address:</strong> {formData.user.address}
              </p>
              <p>
                <strong>Zip Code:</strong> {formData.user.zipCode}
              </p>
            </div>

            <div className={styles.reviewSection}>
              <h4>Tenant Information</h4>
              <p>
                <strong>Tenant Name:</strong> {formData.tenant.tenantName}
              </p>
              <p>
                <strong>Tenant Address:</strong> {formData.tenant.tenantAddress}
              </p>
              <p>
                <strong>Tenant Phone:</strong> {formData.tenant.tenantPhone}
              </p>
            </div>

            <div className={styles.reviewSection}>
              <h4>Subscription Plans</h4>
              {formData.subscriptions.map((plan, index) => (
                <div key={index} className={styles.planReview}>
                  <p>
                    <strong>Plan Name:</strong> {plan.name}
                  </p>
                  <p>
                    <strong>Price:</strong> ${plan.price}
                  </p>
                  <p>
                    <strong>Features:</strong> {plan.features.join(", ")}
                  </p>
                </div>
              ))}
            </div>
          </div>
        );
      case 7:
        return (
          <div className={styles.stepContent}>
            <h3>Payment Details</h3>
            <p>Payment integration will be handled here.</p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.registrationCard}>
        {renderProgressBar()}

        <div className={styles.contentContainer}>{renderStepContent()}</div>

        {currentStep <= 6 && (
          <div className={styles.navigationButtons}>
            <button
              onClick={prevStep}
              disabled={currentStep === 1}
              className={`${styles.navButton} ${styles.prevButton} ${
                currentStep === 1 ? styles.disabled : ""
              }`}
            >
              ← Previous
            </button>

            <button
              onClick={currentStep === 6 ? handleSubmit : nextStep}
              className={`${styles.navButton} ${styles.nextButton}`}
            >
              {currentStep === 6 ? "Complete Onboarding" : "Next Step →"}
            </button>
          </div>
        )}

        {errors.submit && (
          <div className={styles.submitError}>{errors.submit}</div>
        )}
      </div>
    </div>
  );
};

export default OnboardTenant;
