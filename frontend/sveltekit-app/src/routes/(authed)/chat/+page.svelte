<svelte:head>
	<title>Chat Page • Rupee AI</title>
	<meta name="description" content="Chat Page, Rupee AI" />
</svelte:head>

<script>
  import Chatbot from '$lib/components/Chatbot.svelte'

  const aiModels = ['gpt-3.5-turbo', 'gpt-4o', 'fine-tuned-gpt-3.5-turbo', 'gemini-1.5-pro', 'llama-2', 'claude-3'];
  const useCases = ['tax-planning', 'investment'];
  const userAges = ['gen-x', 'millennials', 'gen-z', 'gen-alpha'];
  const userOccupations = ['retired', 'govt-employee', 'private-employee', 'self-employed'];
  const userMonthlySalaries = ['less-than-25k', 'more-than-25k-less-than-50k', 'more-than-50k-less-than-100k', 'more-than-100k']
  const userLanguages = ['english', 'hindi'];

  let selectedUseCase = useCases[0];
  let selectedAiModel = aiModels[0];
  let selectedUserAge = userAges[0];
  let selectedUserOccupation = userOccupations[0];
  let selectedUserMonthlySalary = userMonthlySalaries[0];
  let selectedUserLanguage = userLanguages[0];
</script>

<div class="container mt-3 mb-5">
  <div class="row mx-auto my-3 px-0">
    <div class="col-lg-10">
      <Chatbot aiModelValue={selectedAiModel} useCaseValue={selectedUseCase} userAgeValue={selectedUserAge} userOccupationValue={selectedUserOccupation} userMonthlySalaryValue={selectedUserMonthlySalary} userLanguageValue={selectedUserLanguage} />
    </div>
    <div class="col-lg-2 mt-5 mt-lg-0">
      <h5 class="mb-3">Chat Parameters</h5>

      <form on:submit|preventDefault>
        <p class="my-3">Select AI Model:</p>
        <select class="form-select" name="aiModelInput" aria-label="AI Model" bind:value={selectedAiModel}>
          <option value={aiModels[0]} selected={selectedAiModel === aiModels[0]}>GPT 3.5 Turbo</option>
          <option value={aiModels[1]} selected={selectedAiModel === aiModels[1]}>GPT 4 Omni</option>
          <option value={aiModels[2]} selected={selectedAiModel === aiModels[2]}>Fine Tuned GPT 3.5 Turbo</option>
          <option value={aiModels[3]} selected={selectedAiModel === aiModels[3]} disabled>Google Gemini 1.5 Pro</option>
          <option value={aiModels[4]} selected={selectedAiModel === aiModels[4]} disabled>Meta Llama 2</option>
          <option value={aiModels[5]} selected={selectedAiModel === aiModels[5]} disabled>Anthropic Claude 3</option>
        </select>

        <p class="my-3">Select Use Case:</p>
        <select class="form-select form-select-sm" name="useCaseInput" aria-label="Use Case" bind:value={selectedUseCase}>
          <option value={useCases[0]} selected={selectedUseCase === useCases[0]}>Tax Planning</option>
          <option value={useCases[1]} selected={selectedUseCase === useCases[0]}>Investment</option>
        </select>

        <p class="my-3">Select User Type:</p>
        <select class="form-select form-select-sm" name="userAgeInput" aria-label="User Age" bind:value={selectedUserAge}>
          <option value={userAges[0]} selected={selectedUserAge === userAges[0]}>Gen X (Born 1965 to 1980)</option>
          <option value={userAges[1]} selected={selectedUserAge === userAges[1]}>Millennials (Born 1981 to 1996)</option>
          <option value={userAges[2]} selected={selectedUserAge === userAges[2]}>Gen Z (Born 1997 to 2010)</option>
          <option value={userAges[3]} selected={selectedUserAge === userAges[3]}>Gen Alpha (Born 2011 to 2025)</option>
        </select>

        <select class="form-select form-select-sm" name="userOccupationInput" aria-label="User Occupation" bind:value={selectedUserOccupation}>
          <option value={userOccupations[0]} selected={selectedUserOccupation === userOccupations[0]}>Retired Employee</option>
          <option value={userOccupations[1]} selected={selectedUserOccupation === userOccupations[1]}>Government Employee</option>
          <option value={userOccupations[2]} selected={selectedUserOccupation === userOccupations[2]}>Private Employee</option>
          <option value={userOccupations[3]} selected={selectedUserOccupation === userOccupations[3]}>Self Employed</option>
        </select>

        <select class="form-select form-select-sm" name="userMonthlySalaryInput" aria-label="User Monthly Salary" bind:value={selectedUserMonthlySalary}>
          <option value={userMonthlySalaries[0]} selected={selectedUserMonthlySalary === userMonthlySalaries[0]}>Less than ₹25K</option>
          <option value={userMonthlySalaries[1]} selected={selectedUserMonthlySalary === userMonthlySalaries[1]}>₹25K to ₹50K</option>
          <option value={userMonthlySalaries[2]} selected={selectedUserMonthlySalary === userMonthlySalaries[2]}>₹50K to ₹1L</option>
          <option value={userMonthlySalaries[3]} selected={selectedUserMonthlySalary === userMonthlySalaries[3]}>More than ₹1L</option>
        </select>

        <select class="form-select form-select-sm" name="userLanguageInput" aria-label="User Language" bind:value={selectedUserLanguage}>
          <option value={userLanguages[0]} selected={selectedUserLanguage === userLanguages[0]}>English</option>
          <option value={userLanguages[1]} selected={selectedUserLanguage === userLanguages[1]}>Hindi</option>
        </select>

        <br>

        <button type="submit" class="btn btn-outline-dark">Submit</button>
      </form>
    </div>
  </div>
</div>

<style>
</style>