import React, { useEffect, useState } from 'react';
import axios from 'axios';

function MembershipManagement() {
  const [memberships, setMemberships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMemberships = async () => {
      try {
        const response = await axios.get('http://localhost:8000/memberships', {
          withCredentials: true,
        });
        setMemberships(response.data);
      } catch (err) {
        setError('Failed to fetch memberships.');
      } finally {
        setLoading(false);
      }
    };

    fetchMemberships();
  }, []);

  if (loading) return <p>Loading memberships...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Membership Management</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {memberships.map((membership) => (
            <tr key={membership.id}>
              <td>{membership.id}</td>
              <td>{membership.name}</td>
              <td>{membership.price}</td>
              <td>
                <button>Edit</button>
                <button>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MembershipManagement;