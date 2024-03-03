import { useState } from 'react';
import { Input, Button } from "@material-tailwind/react";

export function Chat() {
  const [query, setQuery] = useState('');

  function handleInputChange(event) {
    setQuery(event.target.value);
  }

  function search(event) {
    event.preventDefault(); 
    alert(`You searched for '${query}'`);
  }

  return (
    <div className="flex justify-center">
      <form onSubmit={search}>
        <div className="relative flex w-full max-w-[60rem]">
          <Input
            className="pr-20"
            type="text"
            name="query"
            label="Enter the Query"
            value={query}
            onChange={handleInputChange}
            containerProps={{
              className: "min-w-0",
            }}
          />
          <Button
            className="!absolute right-1 top-1 rounded"
            size="sm"
            type="submit"
          >
            Submit
          </Button>
        </div>
      </form>
    </div>
  );
}
