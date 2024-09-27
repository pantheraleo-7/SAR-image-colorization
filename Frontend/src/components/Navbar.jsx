import React from "react";

const Navbar = () => {
  return (
    <div>
      <nav class="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600">
        <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
          <span class="self-center text-2xl font-semibold whitespace-nowrap  dark:text-white">
            SAR IMAGE COLORIZER
          </span>
        </div>
      </nav>
    </div>
  );
};

export default Navbar;
