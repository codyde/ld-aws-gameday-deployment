export const isAuthenticated = () => localStorage.getItem('user_key') !== null;
export const getToken = () => localStorage.getItem('user_key');
export const login = user => {
    localStorage.setItem('user_key', JSON.stringify(user));
};
export const logout = () => {
    localStorage.clear();
};