import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getEnv } from '../utils/envUtils';
import styles from '../modules/Register.module.css';
import {Check} from 'lucide-react';

const Register = () => {
  const navigate = useNavigate();
  const tenantId = getEnv('VITE_TENANT_ID');
  const [currentStep, setCurrentStep] = useState(1);
  const [subscriptionPlans, setSubscriptionPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    // Step 1: Subscription Plan
    selectedPlan: '',
    
    // Step 2: Personal Information
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    dateOfBirth: '',
    gender: '',
    address: '',
    city: '',
    zipCode: '',
    
    // Step 3: Account Security
    password: '',
    confirmPassword: '',
    
  });
  const [errors, setErrors] = useState({});
  const [visitedSteps, setVisitedSteps] = useState(new Set([1]));

  const steps = [
    { number: 1, title: 'Plan Selection', icon: '💳' },
    { number: 2, title: 'Personal Info', icon: '👤' },
    { number: 3, title: 'Account Setup', icon: '🔒' },
    { number: 4, title: 'Confirmation', icon: '✅' },
    { number: 5, title: 'Payment Details', icon: '💳' },
  ];

  // Fetch subscription plans from PostgreSQL
  useEffect(() => {
    const fetchPlans = async () => {
      try {
        console.log(getEnv('VITE_API_URL'));
        const response = await fetch(`${getEnv('VITE_API_URL')}/api/subscriptions`, {
          headers: {
            'X-Tenant-ID': tenantId,
            'ngrok-skip-browser-warning': '69420', // Add the custom header here
          },
        });
        
        if (response.ok) {
          const plans = await response.json();
          // Filter out inactive plans in the frontend as a safeguard
          setSubscriptionPlans(plans.filter(plan => plan.is_active));
        } else {
          // Fallback data if API fails
          setSubscriptionPlans([
            {
              id: 'basic',
              name: 'Basic',
              price: 29.99,
              features: ['Access to gym floor', 'Basic equipment', 'Locker access'],
              is_active: true,
              is_popular: false,
            },
            {
              id: 'premium',
              name: 'Premium',
              price: 49.99,
              features: ['All Basic features', 'Group classes', 'Personal trainer consultation', 'Sauna & steam room'],
              is_active: true,
              is_popular: true,
            },
            {
              id: 'elite',
              name: 'Elite',
              price: 79.99,
              features: ['All Premium features', 'Unlimited personal training', 'Nutrition coaching', 'Priority booking', '24/7 access'],
              is_active: false,
              is_popular: false,
            },
          ]);
        }
      } catch (error) {
        console.error('Error fetching subscription plans:', error);
        // Use fallback data
        setSubscriptionPlans([]);
      } finally {
        setLoading(false);
      }
    };

    fetchPlans();
  }, [tenantId]);

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const validateStep = (step) => {
    const newErrors = {};
    
    switch(step) {
      case 1:
        if (!formData.selectedPlan) {
          newErrors.selectedPlan = 'Please select a subscription plan';
        }
        break;
      case 2:
        if (!formData.firstName.trim()) newErrors.firstName = 'First name is required';
        if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required';
        if (!formData.email.trim()) newErrors.email = 'Email is required';
        else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
          newErrors.email = 'Please enter a valid email address';
        }
        if (!formData.phone.trim()) newErrors.phone = 'Phone number is required';
        if (!formData.dateOfBirth) newErrors.dateOfBirth = 'Date of birth is required';
        if (!formData.gender) newErrors.gender = 'Please select gender';
        if (!formData.address.trim()) newErrors.address = 'Address is required';
        if (!formData.city.trim()) newErrors.city = 'City is required';
        if (!formData.zipCode.trim()) newErrors.zipCode = 'ZIP code is required';
        break;
      case 3:
        if (!formData.password) newErrors.password = 'Password is required';
        else if (formData.password.length < 8) newErrors.password = 'Password must be at least 8 characters';
        if (formData.password !== formData.confirmPassword) {
          newErrors.confirmPassword = 'Passwords do not match';
        }
        break;
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const goToStep = (stepNumber) => {
    // Allow navigation to any previously visited step or the next step
    if (visitedSteps.has(stepNumber) || stepNumber === Math.max(...visitedSteps) + 1) {
      setCurrentStep(stepNumber);
      setVisitedSteps(prev => new Set([...prev, stepNumber]));
    }
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      const newStep = currentStep + 1;
      setCurrentStep(newStep);
      setVisitedSteps(prev => new Set([...prev, newStep]));
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    if (!validateStep(4)) return;

    try {
      // Step 1: Register the user and create a pending payment entry
      const registerResponse = await fetch(`${getEnv('VITE_API_URL')}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': tenantId,
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          first_name: formData.firstName,
          last_name: formData.lastName,
          address: formData.address,
          phone: formData.phone,
          subscription_plan_id: formData.selectedPlan,
        }),
      });

      if (!registerResponse.ok) {
        const errorData = await registerResponse.json();
        throw new Error(errorData.message || 'Registration failed');
      }

      // Step 2: Create Stripe Checkout session
      const paymentResponse = await fetch(`${getEnv('VITE_API_URL')}/api/auth/stripe/create-checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': tenantId,
        },
        body: JSON.stringify({
          email: formData.email,
          subscriptionPlanId: formData.selectedPlan,
        }),
      });

      if (!paymentResponse.ok) {
        const errorData = await paymentResponse.json();
        throw new Error(errorData.message || 'Failed to initiate payment');
      }

      const { checkoutUrl } = await paymentResponse.json();
      window.location.href = checkoutUrl; // Redirect to Stripe Checkout
    } catch (error) {
      setErrors({ submit: error.message });
    }
  };

  const toggleGoal = (goal) => {
    const current = formData.fitnessGoals;
    const updated = current.includes(goal)
      ? current.filter(g => g !== goal)
      : [...current, goal];
    updateFormData('fitnessGoals', updated);
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loadingContainer}>
          <div className={styles.loading}>Loading...</div>
        </div>
      </div>
    );
  }

  const renderProgressBar = () => (
    <div className={styles.progressContainer}>
      <div className={styles.progressBar}>
        {steps.map((step, index) => {
          const isActive = currentStep === step.number;
          const isCompleted = currentStep > step.number;
          const isVisited = visitedSteps.has(step.number);
          const isClickable = isVisited || step.number === Math.max(...visitedSteps) + 1;
          
          return (
            <div key={step.number} className={styles.progressItem}>
              <div 
                className={`${styles.progressStep} ${
                  isCompleted ? styles.completed : 
                  isActive ? styles.active : 
                  isVisited ? styles.visited : styles.inactive
                } ${isClickable ? styles.clickable : ''}`}
                onClick={() => isClickable && goToStep(step.number)}
              >
                <span className={styles.stepIcon}>{step.icon}</span>
                <span className={styles.stepNumber}>{step.number}</span>
              </div>
              {index < steps.length - 1 && (
                <div className={`${styles.progressLine} ${isCompleted ? styles.completed : ''}`} />
              )}
            </div>
          );
        })}
      </div>
      <div className={styles.stepInfo}>
        <h2 className={styles.stepTitle}>{steps[currentStep - 1]?.title}</h2>
        <p className={styles.stepCounter}>Step {currentStep} of {steps.length}</p>
      </div>
    </div>
  );

  const renderStepContent = () => {
    switch(currentStep) {
      case 1:
        return (
          <div className={styles.stepContent}>
            <h3 className={styles.stepHeading}>Choose Your Membership Plan</h3>
            <div className={styles.plansGrid}>
              {subscriptionPlans.map((plan) => (
                <div
                  key={plan.id}
                  onClick={() => updateFormData('selectedPlan', plan.id)}
                  className={`${styles.planCard} ${
                    formData.selectedPlan === plan.id ? styles.selected : ''
                  } ${plan.is_popular ? styles.popular : ''}`}
                >
                  {plan.is_popular && (
                    <div className={styles.popularBadge}>
                      MOST POPULAR
                    </div>
                  )}
                  <div className={styles.planHeader}>
                    <h4 className={styles.planName}>{plan.name}</h4>
                    <div className={styles.planPrice}>
                      <span className={styles.price}>${plan.price}</span>
                      <span className={styles.period}>/month</span>
                    </div>
                  </div>
                  <ul className={styles.planFeatures}>
                    {plan.features?.map((feature, index) => (
                      <li key={index} className={styles.feature}>
                        <span className={styles.checkmark}>✓</span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
            {errors.selectedPlan && (
              <p className={styles.error}>{errors.selectedPlan}</p>
            )}
          </div>
        );

      case 2:
        return (
          <div className={styles.stepContent}>
            <h3 className={styles.stepHeading}>Personal Information</h3>
            <div className={styles.formGrid}>
              <div className={styles.inputGroup}>
                <label className={styles.label}>First Name</label>
                <input
                  type="text"
                  value={formData.firstName}
                  onChange={(e) => updateFormData('firstName', e.target.value)}
                  className={`${styles.input} ${errors.firstName ? styles.inputError : ''}`}
                  placeholder="Enter your first name"
                />
                {errors.firstName && <span className={styles.errorText}>{errors.firstName}</span>}
              </div>
              
              <div className={styles.inputGroup}>
                <label className={styles.label}>Last Name</label>
                <input
                  type="text"
                  value={formData.lastName}
                  onChange={(e) => updateFormData('lastName', e.target.value)}
                  className={`${styles.input} ${errors.lastName ? styles.inputError : ''}`}
                  placeholder="Enter your last name"
                />
                {errors.lastName && <span className={styles.errorText}>{errors.lastName}</span>}
              </div>

              <div className={styles.inputGroup}>
                <label className={styles.label}>Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => updateFormData('email', e.target.value)}
                  className={`${styles.input} ${errors.email ? styles.inputError : ''}`}
                  placeholder="Enter your email"
                />
                {errors.email && <span className={styles.errorText}>{errors.email}</span>}
              </div>

              <div className={styles.inputGroup}>
                <label className={styles.label}>Phone</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => updateFormData('phone', e.target.value)}
                  className={`${styles.input} ${errors.phone ? styles.inputError : ''}`}
                  placeholder="Enter your phone number"
                />
                {errors.phone && <span className={styles.errorText}>{errors.phone}</span>}
              </div>

              <div className={styles.inputGroup}>
                <label className={styles.label}>Date of Birth</label>
                <input
                  type="date"
                  value={formData.dateOfBirth}
                  onChange={(e) => updateFormData('dateOfBirth', e.target.value)}
                  className={`${styles.input} ${errors.dateOfBirth ? styles.inputError : ''}`}
                />
                {errors.dateOfBirth && <span className={styles.errorText}>{errors.dateOfBirth}</span>}
              </div>

              <div className={styles.inputGroup}>
                <label className={styles.label}>Gender</label>
                <select
                  value={formData.gender}
                  onChange={(e) => updateFormData('gender', e.target.value)}
                  className={`${styles.input} ${errors.gender ? styles.inputError : ''}`}
                >
                  <option value="">Select gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
                {errors.gender && <span className={styles.errorText}>{errors.gender}</span>}
              </div>
            </div>

            <div className={styles.addressSection}>
              <div className={styles.inputGroup}>
                <label className={styles.label}>Address</label>
                <input
                  type="text"
                  value={formData.address}
                  onChange={(e) => updateFormData('address', e.target.value)}
                  className={`${styles.input} ${errors.address ? styles.inputError : ''}`}
                  placeholder="Enter your street address"
                />
                {errors.address && <span className={styles.errorText}>{errors.address}</span>}
              </div>

              <div className={styles.formGrid}>
                <div className={styles.inputGroup}>
                  <label className={styles.label}>City</label>
                  <input
                    type="text"
                    value={formData.city}
                    onChange={(e) => updateFormData('city', e.target.value)}
                    className={`${styles.input} ${errors.city ? styles.inputError : ''}`}
                    placeholder="Enter your city"
                  />
                  {errors.city && <span className={styles.errorText}>{errors.city}</span>}
                </div>

                <div className={styles.inputGroup}>
                  <label className={styles.label}>ZIP Code</label>
                  <input
                    type="text"
                    value={formData.zipCode}
                    onChange={(e) => updateFormData('zipCode', e.target.value)}
                    className={`${styles.input} ${errors.zipCode ? styles.inputError : ''}`}
                    placeholder="Enter ZIP code"
                  />
                  {errors.zipCode && <span className={styles.errorText}>{errors.zipCode}</span>}
                </div>
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className={styles.stepContent}>
            <h3 className={styles.stepHeading}>Create Your Account</h3>
            <div className={styles.passwordSection}>
              <div className={styles.inputGroup}>
                <label className={styles.label}>Password</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => updateFormData('password', e.target.value)}
                  className={`${styles.input} ${errors.password ? styles.inputError : ''}`}
                  placeholder="Create a password"
                />
                {errors.password && <span className={styles.errorText}>{errors.password}</span>}
                <p className={styles.hint}>Password must be at least 8 characters long</p>
              </div>

              <div className={styles.inputGroup}>
                <label className={styles.label}>Confirm Password</label>
                <input
                  type="password"
                  value={formData.confirmPassword}
                  onChange={(e) => updateFormData('confirmPassword', e.target.value)}
                  className={`${styles.input} ${errors.confirmPassword ? styles.inputError : ''}`}
                  placeholder="Confirm your password"
                />
                {errors.confirmPassword && <span className={styles.errorText}>{errors.confirmPassword}</span>}
              </div>
            </div>
          </div>
        );

      case 4:
        const selectedPlan = subscriptionPlans.find(p => p.id === formData.selectedPlan);
        return (
          <div className={styles.stepContent}>
            <div className={styles.confirmationContainer}>
              <div className={styles.successIcon}><Check className={styles.icon} /></div>
              <h3 className={styles.confirmationTitle}>Almost there!</h3>
              <p className={styles.confirmationText}>Your registration is complete. Here's a summary of your membership:</p>
              
                <div className={styles.card}>
                <h4 className={styles.title}>
                  {selectedPlan?.name} Membership
                </h4>
                <p className={styles.price}>
                  ${selectedPlan?.price}/month
                </p>
                <p className={styles.welcome}>
                  Full name: {formData.firstName} {formData.lastName}
                  <br />Birthday: {formData.dateOfBirth}
                  <br />Email: {formData.email}
                  <br />Address: {formData.address}
                  <br />ZIP code: {formData.zipCode}
                  <br />Phone: {formData.phone}

                </p>
                </div>

              <div className={styles.confirmationDetails}>
                <p>A confirmation email will be sent to {formData.email}</p>
                <p>Upon confirmation, you can start using your membership immediately!</p>
              </div>

              {/* <button 
                className={styles.dashboardButton}
                onClick={() => navigate('/dashboard')}
              >
                Go to Dashboard
              </button> */}
            </div>
          </div>
        );

      case 5:
        return (
          <div className={styles.stepContent}>
            <h3 className={styles.stepHeading}>Enter Payment Details</h3>
            <p className={styles.stepDescription}>Please provide your payment information to complete the registration.</p>
            <div className={styles.paymentFormContainer}>
              {/* Placeholder for Stripe Elements */}
              <p>Stripe payment form will go here.</p>
            </div>
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
        
        <div className={styles.contentContainer}>
          {renderStepContent()}
        </div>

        {currentStep < 5 && (
          <div className={styles.navigationButtons}>
            <button
              onClick={prevStep}
              disabled={currentStep === 1}
              className={`${styles.navButton} ${styles.prevButton} ${
                currentStep === 1 ? styles.disabled : ''
              }`}
            >
              ← Previous
            </button>

            <button
              onClick={currentStep === 4 ? handleSubmit : nextStep}
              className={`${styles.navButton} ${styles.nextButton}`}
            >
              {currentStep === 4 ? 'Complete Registration' : 'Next Step →'}
            </button>
          </div>
        )}

        {errors.submit && (
          <div className={styles.submitError}>
            {errors.submit}
          </div>
        )}
      </div>
    </div>
  );
};

export default Register;