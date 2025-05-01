async function fetchUserData() {
  try {
    const userPromise = await fetch("http://127.0.0.1:5000/api/moj/users").then(
      (data) => data.json(),
    );

    return userPromise;
  } catch (error) {
    console.log(error);
  }
}

async function fetchNumberOfUsers() {
  try {
    const userPromise = await fetch("http://127.0.0.1:5000/api/moj/users")
      .then((data) => data.json())
      .then((result) => result.length);

    return userPromise;
  } catch (error) {
    console.log(error);
  }
}

async function fetchJokesData() {
  try {
    const userPromise = await fetch("http://127.0.0.1:5000/api/moj/jokes").then(
      (data) => data.json(),
    );

    return userPromise;
  } catch (error) {
    console.log(error);
  }
}

async function fetchNumberOfJokes() {
  try {
    const userPromise = await fetch("http://127.0.0.1:5000/api/moj/jokes")
      .then((data) => data.json())
      .then((result) => result.length);

    return userPromise;
  } catch (error) {
    console.log(error);
  }
}

export {
  fetchUserData,
  fetchNumberOfUsers,
  fetchJokesData,
  fetchNumberOfJokes,
};
