select = document.getElementById("tags")
selectedTags = document.createElement("div")
selectedTags.className ="selected-tags"

const hiddenInput =document.querySelector(".tags_values")
select.parentElement.after(selectedTags);

const selectedValues = new Set();
function update_input(){
  
    hiddenInput.value = Array.from(selectedValues).join(",");
}
select.onchange = ()=>{
const selectedOption = select.options[select.selectedIndex];
    const value = selectedOption.value;
    
    if (value && !selectedValues.has(value)) {
      selectedValues.add(value);

      const tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = selectedOption.textContent;

      const remove = document.createElement('span');
      remove.className = 'remove';
      remove.textContent = '×';
      remove.onclick = () => {
        tag.remove();
        selectedValues.delete(value);
        update_input();
      };
      update_input();
      tag.appendChild(remove);
      selectedTags.appendChild(tag);
      select.selectedIndex = 0;
    }
}
